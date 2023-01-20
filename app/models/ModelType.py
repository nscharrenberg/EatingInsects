from django.db import models


class ModelType(models.TextChoices):
    SNN = 'SNN', 'Sequential Neural Network',
    SNN2 = 'SNN2', 'Sequential Neural Network Version 2',
    RF = 'RF', 'Random Forests'
    DT = "DT", 'Decision Tree'
    LR = 'LR', 'Linear Regression'

