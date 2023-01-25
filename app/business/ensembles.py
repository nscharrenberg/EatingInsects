import numpy as np

from app.business import predictors
from app.models import EnsembleModel, EnsembleModelType

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
    ensembleStyle = form['ensemblestyle'].value()

    found_ensemble = get_by_name(name)

    if found_ensemble:
        raise Exception("Ensemble with name {} already exists".format(name))

    ensemble = EnsembleModel(name=name)
    ensemble.save()

    ensemble.ensembleStyle = ensembleStyle
    
    for predictor in predictors:
        ensemble.predictors.add(predictor)

    return ensemble

def load_network(style):
    if style == EnsembleModelType.WA.value:
        return 'WA'
    if style == EnsembleModelType.AVG.value:
        return 'AVG'


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

    style = load_network(ensemble.ensembleStyle)
    predictions = []
    sum_val = 0
    invWeights = []

    for predictor in ensemble.predictors.all():
        cleaned_data['selected_model'] = predictor
        prediction = predictors.predict(form)
        predictions.append(prediction)
        invWeights.append(predictor.rmse)
        sum_val += prediction.solubility

    reWeights = [1-float(x)/float(sum_val) for x in invWeights]
    weights = [x/sum(reWeights) for x in reWeights]

    result = 0
    
    if(style == 'AVG'):    # normal averaging
        avg = sum_val / len(predictions)
        avg = round(float(avg), 2)
        result = avg
    else:    # weighted averaging
        wavg = 0

        for i, predict in enumerate(predictions):
            wavg += float(predict.solubility)*weights[i]

        wavg = round(float(wavg),2)
        result = wavg

    return result, predictions
