# Generated by Django 4.2.1 on 2024-05-31 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('staff', 'Staff'), ('customer', 'Customer')], default='customer', max_length=10),
        ),
    ]
