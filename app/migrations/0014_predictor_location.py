# Generated by Django 4.1.5 on 2023-01-16 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_predictor_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictor',
            name='location',
            field=models.TextField(null=True),
        ),
    ]
