# Generated by Django 5.1.3 on 2024-11-25 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_user_is_adult_user_cin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='CIN',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
    ]
