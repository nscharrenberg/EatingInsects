from django.urls import path

from . import views

urlpatterns = [
    path('models/create', views.CreateModelView.as_view(), name='create_model'),
    path('models/update/<slug:slug>', views.UpdateModelView.as_view(), name='update_model'),
    path('models/delete/<slug:slug>', views.DeleteModelView.as_view(), name='delete_model'),
    path('models', views.ModelsOverviewView.as_view(), name='all_model'),
    path('experiments', views.ExperimentsView.as_view(), name="experiments"),
    path('', views.PredictionView.as_view(), name="make_prediction"),
    path('ensembles', views.EnsembleOverviewView.as_view(), name='all_ensemble'),
    path('ensembles/predict', views.EnsemblePredictionView.as_view(), name='predict_ensemble'),
    path('ensembles/create', views.CreateEnsembleView.as_view(), name='create_ensemble')
]