from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('models/create', views.create_model, name='create_model'),
    path('models/update/<slug:slug>', views.update_model, name='update_model'),
    path('models/delete/<slug:slug>', views.delete_model, name='delete_model'),
    path('models', views.models_overview, name='all_model'),
    path('', views.models_overview, name="make_prediction")
]