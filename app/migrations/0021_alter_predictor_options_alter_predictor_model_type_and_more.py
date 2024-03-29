# Generated by Django 4.1.5 on 2023-01-24 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_protein_predictor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='predictor',
            options={'ordering': ['slug', 'created_at', 'rmse']},
        ),
        migrations.AlterField(
            model_name='predictor',
            name='model_type',
            field=models.TextField(choices=[('SNN', 'Sequential Neural Network'), ('SNN2', 'Sequential Neural Network Version 2'), ('RF', 'Random Forests'), ('DT', 'Decision Tree')]),
        ),
        migrations.AlterField(
            model_name='predictor',
            name='prediction_type',
            field=models.TextField(choices=[('SOL', 'solubility')], default='SOL'),
        ),
    ]
