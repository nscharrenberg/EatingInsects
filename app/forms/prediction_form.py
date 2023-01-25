from django import forms
from django.forms import Form

from app.business import predictors, ensembles


class PredictionForm(Form):
    selected_model = forms.ModelChoiceField(queryset=predictors.get_published(),
                                            empty_label="Select a Model",
                                            label='Your Model to predict with', required=False,
                                            widget=forms.Select(attrs={'class': 'form-control'}))

    select_ensemble = forms.ModelChoiceField(queryset=ensembles.get_all(),
                                             empty_label="Select an Ensemble Model",
                                             label='Your ensemble model to predict with', required=False,
                                             widget=forms.Select(attrs={'class': 'form-control'}))

    yield_um = forms.DecimalField(decimal_places=2, max_digits=12,
                                  initial=1.2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))

    yield_ml = forms.DecimalField(decimal_places=2, max_digits=12,
                                  initial=10,
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))

    calculated_mw = forms.DecimalField(decimal_places=2, max_digits=12,
                                       initial=7.8,
                                       widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))

    calculated_pi = forms.DecimalField(decimal_places=2, max_digits=12,
                                       initial=8.7,
                                       widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))

    gene_product_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, initial='t')
    gene_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial='aaeX')
    cell_location = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    amino_acid_sequence = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial='MSLFPVIVVFGLSFPPIFFELLLSLAIFWLVRRVLVPTGIYDFVWHPALFNTALYCCLFYLISRLFV')
    organism = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
