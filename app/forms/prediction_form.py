from django import forms
from django.forms import Form

from app.models import Predictor
from app.models.PredictionStatus import PredictionStatus


class PredictionForm(Form):
    selected_model = forms.ChoiceField(choices=Predictor.objects.filter(status=PredictionStatus.SAVED.value).values_list('id', 'slug'),
                                       label='Your Model to predict with', required=True,
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    yield_um = forms.DecimalField(decimal_places=2, max_digits=12, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))
    yield_ml = forms.DecimalField(decimal_places=2, max_digits=12, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))
    calculated_mw = forms.DecimalField(decimal_places=2, max_digits=12, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))
    calculated_pi = forms.DecimalField(decimal_places=2, max_digits=12, widget=forms.NumberInput(attrs={'class': 'form-control',  'step': 'any'}))
    sequence_length = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sequence_mass = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gene_product_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    gene_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cell_location = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    amino_acid_sequence = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    organism = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))




