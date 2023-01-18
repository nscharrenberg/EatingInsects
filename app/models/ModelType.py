from django.db import models


class ModelType(models.TextChoices):
    SNN = 'SNN', 'Sequential Neural Network',
    SNN2 = 'SNN2', 'Sequential Neural Network Version 2',
    RF = 'RF', 'Random Forests'
    DNN = 'DNN', 'Deep Neural Network'
