from django import forms
from django.forms import Form


class UploadDatasetForm(Form):
    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'myfile.txt'}))

    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
