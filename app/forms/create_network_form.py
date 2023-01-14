from django import forms
from django.forms import Form

from app.models import ModelType, PredictionType


class CreateNetworkForm(Form):
    selected_model = forms.ChoiceField(choices=ModelType.choices,
                                       label='Your Model to predict with', required=True, initial=ModelType.SNN,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    selected_prediction_type = forms.ChoiceField(choices=PredictionType.choices,
                                                 label='The type of property you want to predict', required=True,
                                                 initial=PredictionType.SOLUBILITY,
                                                 widget=forms.Select(attrs={'class': 'form-control'}))
    version = forms.SlugField(label='version', initial='', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))


