from django.db import models


class Dataset(models.Model):
    name = models.TextField()
    location = models.FileField(upload_to='datasets')
    created_at = models.DateTimeField(auto_now_add=True)
