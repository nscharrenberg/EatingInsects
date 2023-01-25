from django import forms
from django.forms import Form

from app.business import predictors
from app.models import EnsembleModelType


class CreateEnsembleForm(Form):
    selected_models = forms.ModelMultipleChoiceField(queryset=predictors.get_published(),
                                                     label='The models to ensemble', required=True,
                                                     widget=forms.CheckboxSelectMultiple(
                                                         attrs={'class': 'form-check', 'multiple': 'true'}))

    ensemblestyle = forms.ChoiceField(choices=EnsembleModelType.choices, required=True, initial=EnsembleModelType.WA,
                                      label='ensemblestyle', widget=forms.Select(attrs={'class': 'form-control'}))

    name = forms.SlugField(label='name', initial='', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
