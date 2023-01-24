from django.shortcuts import render
from django.views.generic import FormView

from app.business import ensembles
from app.forms.prediction_form import PredictionForm


class EnsemblePredictionView(FormView):
    template_name = "prediction/ensemble.html"

    def get_context_data(self, **kwargs):
        form = PredictionForm()

        context = {
            'form': form
        }

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_page(request, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = PredictionForm(request.POST)
        context['form'] = form

        if form.is_valid():
            context['prediction'], context['predictions'] = ensembles.predict(form)

        return self.render_page(request, context)

    def render_page(self, request, context):
        return render(request, self.template_name, context)
