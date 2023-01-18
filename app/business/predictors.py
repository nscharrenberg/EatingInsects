import pandas as pd

from app.forms.config_model_form import ConfigModelForm
from app.forms.create_network_form import CreateNetworkForm
from app.models import Predictor, Protein, ModelType
from app.models.Dataset import Dataset
from app.models.PredictionStatus import PredictionStatus
from app.networks.SNN.snn import SNN


def get_all():
    return Predictor.objects.all()


def get_published():
    return Predictor.objects.filter(status=PredictionStatus.SAVED.value).all()


def get_by_slug(slug):
    return Predictor.objects.get(slug=slug)


def get_by_id(id):
    return Predictor.objects.get(id=id)


def get_by_amino_acid_and_predictor(predictor: Predictor, sequence: str) -> Protein|None:
    try:
        return Protein.objects.get(predictor=predictor, amino_acid_sequence=sequence)
    except Exception:
        return None


def predict(form) -> Protein:
    amino_acid_sequence = form['amino_acid_sequence'].value()
    model = get_by_id(form['selected_model'].value())

    found_protein = get_by_amino_acid_and_predictor(model, amino_acid_sequence)

    if found_protein:
        return found_protein

    amino_acid_features = extract_amino_acid_features(amino_acid_sequence)

    # TODO: CHeck if Protein is already predicted
    protein = Protein(yield_ml=form['yield_ml'].value(),
                      yield_um=form['yield_um'].value(),
                      calculated_mw=form['calculated_mw'].value(),
                      calculated_pi=form['calculated_pi'].value(),
                      sequence_length=amino_acid_features['sequence_length'],
                      sequence_mass=amino_acid_features['sequence_mass'],
                      gene_product_type=form['gene_product_type'].value(),
                      gene_name=form['gene_name'].value(),
                      cell_location=form['cell_location'].value(),
                      amino_acid_sequence=amino_acid_sequence,
                      organism=form['organism'].value(),
                      steric_parameter=amino_acid_features['steric'],
                      polarizability=amino_acid_features['polarizability'],
                      volume=amino_acid_features['volume'],
                      hydrophobicity=amino_acid_features['hydrophobicity'],
                      helix_probability=amino_acid_features['helix'],
                      sheet_probability=amino_acid_features['sheet'],
                      predictor=model)

    network = load_network(model)
    predictions = network.predict(protein)

    protein.solubility = round(float(predictions[0][0]), 4)
    protein.save()

    return protein


def create_model(form: CreateNetworkForm) -> Predictor:
    if not form:
        raise Exception("Form can not be empty")

    if not form.is_valid():
        raise Exception(form.errors)

    model_type = form['selected_model'].value()
    prediction_type = form['selected_prediction_type'].value()

    version = None

    if form['version'].value():
        version = form['version'].value()

        if is_model_exists(model_type=model_type, prediction_type=prediction_type, version=version):
            raise Exception("The selected model and prediction with the given version already exists.")

    predictor = Predictor(model_type=model_type,
                          prediction_type=prediction_type,
                          version=version)
    predictor.save()

    # Generate an easy to find sluggable
    predictor.slug = generate_slug(predictor)
    predictor.save()

    return predictor


def attach_dataset(slug: str, dataset: Dataset) -> Predictor:
    model = get_by_slug(slug)

    if model.status != PredictionStatus.NEW.value:
        raise Exception("A dataset has already been attached to this model and can not be changed.")

    model.dataset = dataset
    model.status = PredictionStatus.UPLOADED
    model.save()

    return model


def train(slug: str, form: ConfigModelForm) -> Predictor:
    model = get_by_slug(slug)

    if model.status != PredictionStatus.UPLOADED.value:
        raise Exception("Can not train the model because the model has already been trained or the dataset is still "
                        "missing.")

    if not model.dataset:
        model.status = PredictionStatus.NEW.value
        model.save()

        raise Exception("Can not train model as there is no dataset. The status has been set back to NEW so you can "
                        "upload a dataset.")

    model.seed = form['seed'].value()
    model.batch_size = form['batch_size'].value()
    model.split = form['test_split'].value()
    model.epochs = form['epochs'].value()
    model.learning_rate = form['learning_rate'].value()
    model.save()

    load_network(model)

    model.status = PredictionStatus.TRAINED.value
    model.save()

    return model


def test(slug: str) -> Predictor:
    model = get_by_slug(slug)

    network = load_network(model)
    results = network.test()

    model.rmse = results[3]
    model.mae = results[2]

    model.status = PredictionStatus.TESTED.value
    model.save()

    return model


def export(slug: str) -> Predictor:
    model = get_by_slug(slug)

    model.status = PredictionStatus.SAVED.value
    model.save()

    return model


def generate_slug(predictor: Predictor):
    version_label = predictor.version
    if not version_label:
        version_label = predictor.created_at.strftime('%Y%m%d_%H%M')

    return '{}-{}-{}'.format(predictor.model_type, predictor.prediction_type, version_label)


def is_model_exists(model_type: str, prediction_type: str, version: str) -> bool:
    found_models = Predictor.objects.filter(model_type=model_type, prediction_type=prediction_type, version=version)

    if found_models.count() > 0:
        return True

    return False


def load_network(predictor: Predictor):
    if predictor.model_type == ModelType.SNN.value:
        return SNN(predictor)


def extract_data_from_amino_acids(sequence: str):
    sequence_length = len(sequence)
    sequence_mass = 0

    aaInfo = pd.read_csv('resources/private/datasets/aa_data_solubility.csv', sep=',')

    for element in sequence:
        if element == 'X':
            element = 'G'

        try:
            sequence_mass += aaInfo.at[aaInfo.index[aaInfo['abbreviation'] == element][0], 'Molecular weight']
        except Exception:
            print("amino acid \"{}\" could not be found".format(element))

    return {
        'sequence_length': sequence_length,
        'sequence_mass': sequence_mass
    }


def extract_amino_acid_features(sequence: str):
    meta_data = extract_data_from_amino_acids(sequence)

    sequence_length = meta_data['sequence_length']
    sequence_mass = meta_data['sequence_mass']

    aaphy7 = pd.read_csv('resources/private/datasets/aaphy7.csv', sep=',')

    steric = 0
    polarizability = 0
    volume = 0
    hydrophobicity = 0
    helix = 0
    sheet = 0

    for element in sequence:
        if element == 'X':
            element = 'G'

        ind = aaphy7.index[aaphy7['abbreviation'] == element]
        steric += aaphy7.at[ind[0], 'Steric parameter (graph shape index)']
        polarizability += aaphy7.at[ind[0], 'Polarizability']
        volume += aaphy7.at[ind[0], 'Volume (normalized van der Waals volume)']
        hydrophobicity += aaphy7.at[ind[0], 'Hydrophobicity']
        helix += aaphy7.at[ind[0], 'Helix probability']
        sheet += aaphy7.at[ind[0], 'Sheet probability']

    steric = steric / sequence_length
    polarizability = polarizability / sequence_length
    volume = volume / sequence_length
    hydrophobicity = hydrophobicity / sequence_length
    helix = helix / sequence_length
    sheet = sheet / sequence_length

    return {
        'sequence_length': sequence_length,
        'sequence_mass': round(sequence_mass, 4),
        'steric': round(steric, 4),
        'polarizability': round(polarizability, 4),
        'volume': round(volume, 4),
        'hydrophobicity': round(hydrophobicity, 4),
        'helix': round(helix, 4),
        'sheet': round(sheet, 4),
    }
