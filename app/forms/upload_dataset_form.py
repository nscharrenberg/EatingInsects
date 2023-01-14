from django import forms
from django.forms import Form

from app.models import ModelType, PredictionType


class UploadDatasetForm(Form):
    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    file = forms.FileField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file'}))
