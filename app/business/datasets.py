from app.forms.upload_dataset_form import UploadDatasetForm
from app.models.Dataset import Dataset

import pandas as pd

from app.networks.utils.processing_utils import ProcessingUtils


def get_all():
    return Dataset.objects.all()


def upload_dataset(form: UploadDatasetForm) -> Dataset:
    if not form:
        raise Exception("Form can not be empty")

    if not form.is_valid():
        raise Exception(form.errors)

    dataset_file = form['file'].value()
    dataset_name = form['name'].value()

    validate_dataset(dataset_file)

    if not dataset_name:
        dataset_name = dataset_file.name

    dataset = Dataset(name=dataset_name, location=dataset_file)
    dataset.save()

    return dataset


def validate_dataset(file):
    data = pd.read_csv(file)
    expected_columns = ProcessingUtils.get_expected_dataset_columns()
    expected_prediction_columns = ProcessingUtils.get_expected_dataset_prediction_columns()

    missing_columns = []

    for col in expected_columns:
        if col not in data.columns:
            missing_columns.append(col)

    if len(missing_columns) > 0:
        raise Exception("Required columns in the dataset are missing and must be present. Fields that are still "
                        "missing are {}".format(missing_columns))

    prediction_field_exists = False

    for col in expected_prediction_columns:
        if col in data.columns:
            prediction_field_exists = True
            break

    if not prediction_field_exists:
        raise Exception("A prediction field is missing. e.g. solubility")


def read_dataset(dataset: Dataset) -> str:
    uploaded_dataset = dataset.location
    try:
        uploaded_dataset.open('r')
        return uploaded_dataset.read()
    finally:
        uploaded_dataset.close()
