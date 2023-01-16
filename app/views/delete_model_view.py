from django.shortcuts import render
from django.views.generic import FormView


class DeleteModelView(FormView):
    def get(self, request, *args, **kwargs):
        context = {

        }

        return render(request, 'manager/update.html', context)