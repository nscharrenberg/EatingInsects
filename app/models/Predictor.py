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

    seed = models.IntegerField(default=42)
    split = models.DecimalField(default=0.2, decimal_places=2, max_digits=12)
    batch_size = models.IntegerField(default=20)
    epochs = models.IntegerField(default=200)
    learning_rate = models.DecimalField(default=0.01, decimal_places=6, max_digits=12)

    rmse = models.DecimalField(decimal_places=6, max_digits=12, null=True)
    mae = models.DecimalField(decimal_places=6, max_digits=12, null=True)

    def __str__(self):
        return '{}-{}'.format(self.slug, self.status)
