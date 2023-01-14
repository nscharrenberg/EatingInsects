from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('models/create', views.create_model, name='create_model'),
    path('models/update/<slug:slug>', views.train_model, name='train_model'),
    path('models', views.models_overview, name='all_model'),
]