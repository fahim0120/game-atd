# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-05-07 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsentPageResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selectedAnswer', models.CharField(max_length=200)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('durationPage', models.FloatField(blank=True, null=True)),
                ('recordDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ImagePool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageFileName', models.CharField(max_length=250)),
                ('imageId', models.IntegerField()),
                ('enemyOrFriendly', models.CharField(max_length=200)),
                ('countUsage', models.IntegerField(blank=True, null=True)),
                ('whichRoundUsed', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='InstructionPageResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mTurkId', models.CharField(max_length=200)),
                ('groupId', models.CharField(max_length=200)),
                ('numberOfAttempt', models.IntegerField()),
                ('numberOfCorrect', models.IntegerField()),
                ('selectedAnswer', models.CharField(max_length=200)),
                ('durationPage', models.FloatField(blank=True, null=True)),
                ('recordDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='MessagePool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupId', models.CharField(max_length=200, unique=True)),
                ('groupName', models.TextField()),
                ('groupReliability', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mTurkId', models.CharField(max_length=200)),
                ('groupId', models.CharField(max_length=200)),
                ('roundNumber', models.IntegerField()),
                ('imageId', models.IntegerField(blank=True, null=True)),
                ('countZoomIn', models.IntegerField(blank=True, null=True)),
                ('countZoomOut', models.IntegerField(blank=True, null=True)),
                ('answer', models.CharField(max_length=200)),
                ('correctOrNot', models.IntegerField()),
                ('durationToAnswer', models.FloatField()),
                ('responseDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mTurkId', models.CharField(max_length=200)),
                ('groupId', models.CharField(max_length=200)),
                ('roundNumber', models.IntegerField()),
                ('numImgToManual', models.IntegerField(blank=True, null=True)),
                ('numImgToAuto', models.IntegerField(blank=True, null=True)),
                ('durationResults', models.FloatField(blank=True, null=True)),
                ('durationMessage', models.FloatField(blank=True, null=True)),
                ('durationAllocation', models.FloatField(blank=True, null=True)),
                ('durationGamePage', models.FloatField(blank=True, null=True)),
                ('durationResultPage', models.FloatField(blank=True, null=True)),
                ('recordDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mTurkId', models.CharField(max_length=200)),
                ('groupId', models.CharField(max_length=200)),
                ('groupName', models.TextField()),
                ('roundNumber', models.IntegerField()),
                ('numImgAllocatedManual', models.IntegerField(blank=True, null=True)),
                ('numImgAllocatedAuto', models.IntegerField(blank=True, null=True)),
                ('numImgCorrectManual', models.IntegerField(blank=True, null=True)),
                ('numImgCorrectAuto', models.IntegerField(blank=True, null=True)),
                ('numImgIncorrectManual', models.IntegerField(blank=True, null=True)),
                ('numImgIncorrectAuto', models.IntegerField(blank=True, null=True)),
                ('totalTimeManual', models.FloatField(blank=True, null=True)),
                ('totalTimeAuto', models.FloatField(blank=True, null=True)),
                ('avgTimeManual', models.FloatField(blank=True, null=True)),
                ('avgTimeAuto', models.FloatField(blank=True, null=True)),
                ('totalTime', models.FloatField(blank=True, null=True)),
                ('rawScore', models.FloatField(blank=True, null=True)),
                ('noiseScore', models.FloatField(blank=True, null=True)),
                ('roundScore', models.FloatField(blank=True, null=True)),
                ('trajectory', models.TextField()),
                ('recordDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mTurkId', models.CharField(max_length=200)),
                ('groupId', models.CharField(max_length=200)),
                ('groupName', models.TextField()),
                ('dateParticipated', models.DateTimeField()),
            ],
        ),
    ]