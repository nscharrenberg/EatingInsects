from django.db import models


class PredictionStatus(models.TextChoices):
    NEW = 'NEW', 'Newly Created'
    TRAINED = 'TRAINED', 'Trained'
    TESTED = 'TESTED', 'Tested'
    SAVED = 'SAVED', 'Model Saved'
