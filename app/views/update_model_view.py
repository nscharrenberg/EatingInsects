from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView
from django import forms

from app.business import predictors, datasets
from app.forms.config_model_form import ConfigModelForm
from app.forms.upload_dataset_form import UploadDatasetForm
from app.models import ModelType, PredictionType
from app.models.PredictionStatus import PredictionStatus


class UpdateModelView(FormView):
    template_name = "manager/update.html"

    def get_context_data(self, **kwargs):
        model = predictors.get_by_slug(self.kwargs['slug'])

        models = ModelType.choices
        prediction_types = PredictionType.choices

        model_type_field = forms.ChoiceField(choices=ModelType.choices,
                                             widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'true'}))

        prediction_type_field = forms.ChoiceField(choices=PredictionType.choices,
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control', 'disabled': 'true'}))

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
            context['upload_form'] = UploadDatasetForm()
        else:
            context['dataset'] = datasets.read_dataset(model.dataset)

        if model.status == PredictionStatus.UPLOADED.value:
            context['config_form'] = ConfigModelForm()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_page(request, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        model = context['model']

        if model.status == PredictionStatus.NEW.value:
            uploaded_form = UploadDatasetForm(request.POST, request.FILES)
            context['upload_form'] = uploaded_form

            if uploaded_form.is_valid():
                try:
                    dataset = datasets.upload_dataset(uploaded_form)
                    model = predictors.attach_dataset(model.slug, dataset)
                    messages.success(request,
                                     'Dataset "{}" has been uploaded for {}'.format(dataset.name, model.slug))
                except Exception as error:
                    messages.error(request, str(error))
        elif model.status == PredictionStatus.UPLOADED.value:
            config_form = ConfigModelForm(request.POST)
            context['config_form'] = config_form

            if config_form.is_valid():
                try:
                    model = predictors.train(model.slug, config_form)
                    messages.success(request, "The model has been configured and trained on the dataset.")
                except Exception as error:
                    messages.error(request, str(error))
        elif model.status == PredictionStatus.TRAINED.value:
            model = predictors.test(model.slug)
            messages.success(request, "The model has been tested and the performance has been calculated.")
        elif model.status == PredictionStatus.TESTED.value:
            model = predictors.export(model.slug)
            messages.success(request, "The model has been exported and can now be used throughout the system")

        return redirect('update_model', slug=model.slug)

    def render_page(self, request, context):
        return render(request, self.template_name, context)
