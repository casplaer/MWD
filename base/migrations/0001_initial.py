# Generated by Django 5.0.6 on 2024-05-30 20:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=700)),
                ('price', models.FloatField()),
                ('unit', models.CharField(choices=[('pcs', 'Pieces'), ('kg', 'Kilogram'), ('l', 'Liter')], max_length=3)),
                ('category', models.CharField(choices=[('cat1', 'Category 1'), ('cat2', 'Category 2'), ('cat3', 'Category 3')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20, verbose_name='User contact phone number')),
                ('name', models.CharField(max_length=100, verbose_name='User full name')),
                ('id_user', models.IntegerField()),
                ('address', models.CharField(max_length=200, verbose_name='User full address')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]