from django.shortcuts import render, redirect
from django.contrib import messages

from app.business import predictors
from app.forms.manager_form import CreateNetworkForm
from app.models import PredictionType, ModelType, Predictor


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
    context = {

    }

    return render(request, 'manager/update.html', context)


# Delete the selected Network Model Definition and its models
def delete_model(request, slug):
    context = {

    }

    return render(request, 'manager/update.html', context)
