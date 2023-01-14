from app.forms.create_network_form import CreateNetworkForm
from app.models import Predictor


def get_all():
    return Predictor.objects.all()


def get_by_slug(slug):
    return Predictor.objects.get(slug=slug)


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
