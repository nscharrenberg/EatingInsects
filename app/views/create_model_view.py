from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import FormView

from app.business import predictors
from app.forms.create_network_form import CreateNetworkForm
from app.models import ModelType, PredictionType


class CreateModelView(FormView):
    template_name = "manager/builder.html"

    def get_context_data(self, **kwargs):
        models = ModelType.choices
        prediction_types = PredictionType.choices

        context = {
            'models': models,
            'prediction_types': prediction_types,
        }

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = CreateNetworkForm()

        return self.render_page(request, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = CreateNetworkForm(request.POST)
        context['form'] = form

        if form.is_valid():
            try:
                created = predictors.create_model(form)
                messages.success(request, '{} has been successfully created'.format(created))

                return redirect('all_model')
            except Exception as error:
                messages.error(request, str(error))

                return redirect('create_model')
        else:
            return self.render_page(request, context)

    def render_page(self, request, context):
        return render(request, self.template_name, context)
