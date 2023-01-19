from django.db import models


class PredictionType(models.TextChoices):
    SOLUBILITY = 'SOL', 'solubility',
