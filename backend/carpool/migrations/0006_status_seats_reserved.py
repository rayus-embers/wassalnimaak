# Generated by Django 5.1.3 on 2024-12-18 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0005_alter_covoiturage_addresses'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='seats_reserved',
            field=models.PositiveIntegerField(default=1),
        ),
    ]