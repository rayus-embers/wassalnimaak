# Generated by Django 5.1.3 on 2024-12-16 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='is_read',
            new_name='read',
        ),
    ]