# Generated by Django 5.1.3 on 2024-11-25 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_driver_banned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_adult',
        ),
        migrations.AddField(
            model_name='user',
            name='CIN',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
