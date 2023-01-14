from django.db import models

from app.models.Dataset import Dataset
from app.models.ModelType import ModelType
from app.models.PredictionStatus import PredictionStatus
from app.models.PredictionType import PredictionType


class Predictor(models.Model):
    model_type = models.TextField(choices=ModelType.choices)
    prediction_type = models.TextField(default=PredictionType.SOLUBILITY.value, choices=PredictionType.choices)
    version = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.FileField(null=True)
    status = models.TextField(default=PredictionStatus.NEW.value, choices=PredictionStatus.choices)
    slug = models.SlugField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{}-{}'.format(self.slug, self.status)
