from django.db import models


class EnsembleModelType(models.TextChoices):
    WA = 'WA', 'Weighted Average',
    AVG = 'AVG', 'Standard Average',

