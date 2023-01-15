from app.forms.upload_dataset_form import UploadDatasetForm
from app.models import Predictor
from app.models.Dataset import Dataset


def get_all():
    return Dataset.objects.all()


def upload_dataset(form: UploadDatasetForm) -> Dataset:
    if not form:
        raise Exception("Form can not be empty")

    if not form.is_valid():
        raise Exception(form.errors)

    dataset_file = form['file'].value()
    dataset_name = form['name'].value()

    if not dataset_name:
        dataset_name = dataset_file.name

    dataset = Dataset(name=dataset_name, location=dataset_file)
    dataset.save()

    return dataset
