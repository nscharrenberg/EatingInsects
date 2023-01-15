import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms

from app.business import predictors, datasets
from app.forms.create_network_form import CreateNetworkForm
from app.forms.upload_dataset_form import UploadDatasetForm
from app.models import PredictionType, ModelType, Predictor
from app.models.Dataset import Dataset
from app.models.PredictionStatus import PredictionStatus


def models_overview(request):
    models = predictors.get_all()

    context = {
        'models': models
    }

    return render(request, 'manager/list.html', context)


# Create the Network Model Definition ready to be trained and saved.
def create_model(request):
    models = ModelType.choices
    prediction_types = PredictionType.choices

    form = CreateNetworkForm()

    if request.method == 'POST':
        form = CreateNetworkForm(request.POST)

        if form.is_valid():
            try:
                created = predictors.create_model(form)
                messages.success(request, '{} has been successfully created'.format(created))

                return redirect('all_model')
            except Exception as error:
                messages.error(request, str(error))

                return redirect('create_model')

    context = {
        'models': models,
        'prediction_types': prediction_types,
        'form': form
    }

    return render(request, 'manager/builder.html', context)


# Update the selected Network Model Definition
def update_model(request, slug):
    model = predictors.get_by_slug(slug)

    models = ModelType.choices
    prediction_types = PredictionType.choices

    model_type_field = forms.ChoiceField(choices=ModelType.choices,
                                         widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'true'}))

    prediction_type_field = forms.ChoiceField(choices=PredictionType.choices,
                                              widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'true'}))

    version_field = forms.SlugField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true'}))
    version_or_timestamp = model.created_at.strftime('%Y%m%d_%H%M')

    if model.version:
        version_or_timestamp = model.version

    context = {
        'model': model,
        'models': models,
        'prediction_types': prediction_types,
        'model_field': model_type_field.widget.render('model_field', model.model_type),
        'prediction_field': prediction_type_field.widget.render('prediction_field', model.prediction_type),
        'version_field': version_field.widget.render('version_field', version_or_timestamp),
        'PredictionStatus': PredictionStatus
    }

    if model.status == PredictionStatus.NEW.value:
        if request.method == 'POST':
            uploaded_form = UploadDatasetForm(request.POST, request.FILES)
            context['upload_form'] = uploaded_form

            if uploaded_form.is_valid():
                try:
                    dataset = datasets.upload_dataset(uploaded_form)

                    model = predictors.attach_dataset(model.slug, dataset)

                    messages.success(request, 'Dataset "{}" has been uploaded for {}'.format(dataset.name, model.slug))
                except Exception as error:
                    messages.error(request, str(error))

                return redirect('update_model', slug=model.slug)
        else:
            context['upload_form'] = UploadDatasetForm()
    else:
        uploaded_dataset = model.dataset.location
        try:
            uploaded_dataset.open('r')
            context['dataset'] = uploaded_dataset.read()
        finally:
            uploaded_dataset.close()

    if model.status == PredictionStatus.UPLOADED.value:
        print("Dataset uploaded. You need to train the model on the dataset before continueing.")
    elif model.status == PredictionStatus.TRAINED.value:
        print("Trained you can now both test and save the model")
    elif model.status == PredictionStatus.TESTED.value:
        print("Tested you can now save the model")
    elif model.status == PredictionStatus.SAVED.value:
        print("Saved nothing more to do")
    else:
        print("Error")

    return render(request, 'manager/update.html', context)


# Delete the selected Network Model Definition and its models
def delete_model(request, slug):
    context = {

    }

    return render(request, 'manager/update.html', context)
