import numpy as np

from app.business import predictors
from app.models.EnsembleModel import EnsembleModel

import pandas as pd


def get_all():
    return EnsembleModel.objects.all()


def get_by_id(id):
    return EnsembleModel.objects.get(id=id)


def get_by_name(name):
    try:
        return EnsembleModel.objects.get(name=name)
    except Exception:
        return None


def create(form) -> EnsembleModel:
    if not form:
        raise Exception("Form can not be empty")

    if not form.is_valid():
        raise Exception(form.errors)

    predictors = form['selected_models'].value()
    name = form['name'].value()

    found_ensemble = get_by_name(name)

    if found_ensemble:
        raise Exception("Ensemble with name {} already exists".format(name))

    ensemble = EnsembleModel(name=name)
    ensemble.save()

    for predictor in predictors:
        ensemble.predictors.add(predictor)

    return ensemble


def predict(form):
    if not form:
        raise Exception("Form can not be empty")

    if not form.is_valid():
        raise Exception(form.errors)

    cleaned_data = form.cleaned_data

    form_ensemble = cleaned_data['select_ensemble']

    if not form_ensemble:
        raise Exception("An Ensemble Model must be selected")

    ensemble = get_by_id(form_ensemble.id)

    predictions = []
    sum_val = 0

    for predictor in ensemble.predictors.all():
        cleaned_data['selected_model'] = predictor
        prediction = predictors.predict(form)

        predictions.append(prediction)
        sum_val += prediction.solubility

    # averaging
    avg = sum_val / len(predictions)
    avg = round(float(avg), 2)

    return avg, predictions
