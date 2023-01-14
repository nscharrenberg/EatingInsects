from django.contrib import admin

# Register your models here.
from app.models import Predictor, Protein

admin.register(Predictor)
admin.register(Protein)