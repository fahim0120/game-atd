# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-07-13 02:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='noiseScore',
            new_name='accScore',
        ),
        migrations.RenameField(
            model_name='score',
            old_name='rawScore',
            new_name='timeScore',
        ),
    ]
