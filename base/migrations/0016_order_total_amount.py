# Generated by Django 5.0.6 on 2024-05-31 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_cart_is_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.FloatField(default=0.0),
        ),
    ]