from django.db import models

from app.models.Predictor import Predictor


class EnsembleModel(models.Model):
    name = models.TextField()
    predictors = models.ManyToManyField(Predictor)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)
