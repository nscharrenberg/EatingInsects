from django.shortcuts import render
from django.views.generic import TemplateView

from app.business import predictors


class ModelsOverviewView(TemplateView):
    template_name = "manager/list.html"

    def get_context_data(self, **kwargs):
        models = predictors.get_all()

        context = {
            'models': models
        }

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_page(request, context)

    def render_page(self, request, context):
        return render(request, self.template_name, context)