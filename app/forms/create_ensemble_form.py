from django import forms
from django.forms import Form

from app.business import predictors


class CreateEnsembleForm(Form):
    selected_models = forms.ModelMultipleChoiceField(queryset=predictors.get_published(),
                                                     label='The models to ensemble', required=True,
                                                     widget=forms.CheckboxSelectMultiple(
                                                         attrs={'class': 'form-check', 'multiple': 'true'}))

    name = forms.SlugField(label='name', initial='', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
