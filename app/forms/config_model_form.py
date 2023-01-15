from django import forms
from django.forms import Form


class ConfigModelForm(Form):
    seed = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 42}), required=False, initial=42)
    test_split = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 0.2, 'step': 'any'}), required=False, initial=0.2)
    batch_size = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 20}), required=False, initial=20)
    epochs = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 200}), required=False, initial=200)
    learning_rate = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 0.01, 'step': 'any'}), required=False, initial=0.01)
