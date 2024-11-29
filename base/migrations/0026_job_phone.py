# Generated by Django 5.0.6 on 2024-11-29 11:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_slidersettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='phone',
            field=models.CharField(default=375333886307, max_length=13, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть в формате +375XXXXXXXXX.', regex='^\\+375\\d{9}$')]),
            preserve_default=False,
        ),
    ]