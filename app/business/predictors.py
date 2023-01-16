from app.forms.config_model_form import ConfigModelForm
from app.forms.create_network_form import CreateNetworkForm
from app.models import Predictor, Protein
from app.models.Dataset import Dataset
from app.models.PredictionStatus import PredictionStatus
from app.networks.SNN.snn import SNN


def get_all():
    return Predictor.objects.all()


def get_published():
    return Predictor.objects.filter(status=PredictionStatus.SAVED.value).all()


def get_by_slug(slug):
    return Predictor.objects.get(slug=slug)


def predict(form) -> Protein:
    # TODO: CHeck if Protein is already predicted
    protein = Protein(yield_ml=form['yield_ml'].value(),
                      yield_um=form['yield_um'].value(),
                      calculated_mw=form['calculated_mw'].value(),
                      calculated_pi=form['calculated_pi'].value(),
                      sequence_length=form['sequence_length'].value(),
                      sequence_mass=form['sequence_mass'].value(),
                      gene_product_type=form['gene_product_type'].value(),
                      gene_name=form['gene_name'].value(),
                      cell_location=form['cell_location'].value(),
                      amino_acid_sequence=form['amino_acid_sequence'].value(),
                      organism=form['organism'].value())

    # TODO: Make Prediction
    protein.solubility = 0.5
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

    network = SNN(model)

    model.status = PredictionStatus.TRAINED.value
    model.save()

    return model


def test(slug: str) -> Predictor:
    model = get_by_slug(slug)

    network = SNN(model)
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
