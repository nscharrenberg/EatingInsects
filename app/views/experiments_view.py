from django.shortcuts import render
from django.views.generic import FormView

from app.Experiments.GridSearchCV import get_results


class ExperimentsView(FormView):
    template_name = "experiments/results.html"

    def get_context_data(self, **kwargs):
        results = get_results()
        context = {
            'results': results
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_page(request, context)

    def render_page(self, request, context):
        return render(request, self.template_name, context)