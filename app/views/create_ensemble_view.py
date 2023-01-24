from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import FormView

from app.business import predictors, ensembles
from app.forms.create_ensemble_form import CreateEnsembleForm


class CreateEnsembleView(FormView):
    template_name = "ensembles/builder.html"

    def get_context_data(self, **kwargs):
        all_predictors = predictors.get_published()

        context = {
            'predictors': all_predictors
        }

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = CreateEnsembleForm()

        return self.render_page(request, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = CreateEnsembleForm(request.POST)
        context['form'] = form

        if form.is_valid():
            try:
                created = ensembles.create(form)
                messages.success(request, '{} has been successfully created'.format(created))

                return redirect('all_ensemble')
            except Exception as error:
                messages.error(request, str(error))

                return redirect('create_ensemble')
        else:
            return self.render_page(request, context)

    def render_page(self, request, context):
        return render(request, self.template_name, context)
