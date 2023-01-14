from django.db import models


class ModelType(models.TextChoices):
    SNN = 'SNN', 'Sequential Neural Network'
    RF = 'RF', 'Random Forests'
    DNN = 'DNN', 'Deep Neural Network'
