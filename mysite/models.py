from django.db import models
from django.contrib.auth.models import User
import os
import sqlite3
# Create your models here.


class Users(models.Model):
    """
    Create new user.
    Called from register_user function.
    """
    mTurkId = models.CharField(max_length=200)
    groupId = models.CharField(max_length=200)
    groupName = models.TextField()
    dateParticipated = models.DateTimeField()
    #gifOrder = models.TextField()


class Response(models.Model):
    """
    Adds image identification responses of the user
    """
    mTurkId = models.CharField(max_length=200)
    groupId = models.CharField(max_length=200)
    roundNumber = models.IntegerField()
    imageId = models.IntegerField(null=True, blank=True)
    countZoomIn = models.IntegerField(null=True, blank=True)
    countZoomOut = models.IntegerField(null=True, blank=True)
    answer = models.CharField(max_length=200)                  # what does answer store?
    correctOrNot = models.IntegerField()
    durationToAnswer = models.FloatField()
    responseDate = models.DateTimeField()


class Results(models.Model):
    """
    Stores the allocation details.
    Called from the begin function.
    """
    mTurkId = models.CharField(max_length=200)
    groupId = models.CharField(max_length=200)
    roundNumber = models.IntegerField()
    numImgToManual = models.IntegerField(null=True, blank=True)
    numImgToAuto = models.IntegerField(null=True, blank=True)
    durationResults = models.FloatField(null=True, blank=True)
    durationMessage = models.FloatField(null=True, blank=True)
    durationAllocation = models.FloatField(null=True, blank=True)
    durationGamePage = models.FloatField(null=True, blank=True)
    durationResultPage = models.FloatField(null=True, blank=True)
    recordDate = models.DateTimeField()


"""
class Score(models.Model):
    mTurkId = models.CharField(max_length = 200)
    groupId = models.CharField(max_length = 200)
    groupName = models.TextField()
    roundNumber = models.IntegerField()
    numImgAllocatedManual = models.IntegerField(null=True, blank=True)
    numImgAllocatedAuto = models.IntegerField(null=True, blank=True)
    numImgCorrectManual = models.IntegerField(null=True, blank=True)
    numImgCorrectAuto = models.IntegerField(null=True, blank=True)
    numImgIncorrectManual = models.IntegerField(null=True, blank=True)
    numImgIncorrectAuto = models.IntegerField(null=True, blank=True)
    totalTimeManual = models.FloatField(null=True, blank=True)
    totalTimeAuto = models.FloatField(null=True, blank=True)
    avgTimeManual = models.FloatField(null=True, blank=True)
    avgTimeAuto = models.FloatField(null=True, blank=True)
    totalTime = models.FloatField(null=True, blank=True)
    accScore = models.FloatField(null=True, blank=True)
    timeScore = models.FloatField(null=True, blank=True)
    roundScore = models.FloatField(null=True, blank=True)
    trajectory = models.TextField()
    recordDate = models.DateTimeField()
"""

# 07-12-20 10:08 PM
class Score(models.Model):
    """
    Stores the scores after each round.
    Called from the recordAnswers funciton.
    """
    mTurkId = models.CharField(max_length=200)
    groupId = models.CharField(max_length=200)
    groupName = models.TextField()
    roundNumber = models.IntegerField()
    numImgAllocatedManual = models.IntegerField(null=True, blank=True)
    numImgAllocatedAuto = models.IntegerField(null=True, blank=True)
    numImgCorrectManual = models.IntegerField(null=True, blank=True)
    numImgCorrectAuto = models.IntegerField(null=True, blank=True)
    numImgIncorrectManual = models.IntegerField(null=True, blank=True)
    numImgIncorrectAuto = models.IntegerField(null=True, blank=True)
    totalTimeManual = models.FloatField(null=True, blank=True)
    totalTimeAuto = models.FloatField(null=True, blank=True)
    avgTimeManual = models.FloatField(null=True, blank=True)
    avgTimeAuto = models.FloatField(null=True, blank=True)
    totalTime = models.FloatField(null=True, blank=True)
    accScore = models.FloatField(null=True, blank=True)     # 1
    timeScore = models.FloatField(null=True, blank=True)    # 1
    #rawScore = models.FloatField(null=True, blank=True)    # 2
    #noiseScore = models.FloatField(null=True, blank=True)  # 2
    roundScore = models.FloatField(null=True, blank=True)
    trajectory = models.TextField()
    recordDate = models.DateTimeField()


# 05-05-20 10:20 AM
class ImagePool(models.Model):
    """
    Stores the images into db.
    """
    imageFileName = models.CharField(max_length=250)
    imageId = models.IntegerField()
    enemyOrFriendly = models.CharField(max_length=200)
    countUsage = models.IntegerField(null=True, blank=True)
    whichRoundUsed = models.CharField(max_length=250)

    def __unicode__(self):
        return self.imageFileName


# 05-05-20 09:20 AM
class MessagePool(models.Model):
    """
    Stores the experimental group details.
    """
    groupId = models.CharField(max_length=200, unique=True)
    groupName = models.TextField()
    groupReliability = models.CharField(max_length=200)
    message = models.TextField()


class InstructionPageResults(models.Model):
    """
    Stores the questionnaire responses in the instruction page.
    """
    mTurkId = models.CharField(max_length=200)
    groupId = models.CharField(max_length=200)
    numberOfAttempt = models.IntegerField()
    numberOfCorrect = models.IntegerField()
    selectedAnswer = models.CharField(max_length=200)
    durationPage = models.FloatField(null=True, blank=True)
    recordDate = models.DateTimeField()


class CameraPermission(models.Model):
    """
    Stores whether the camera permission was allowed.
    """
    mTurkId = models.CharField(max_length=200)
    groupId = models.CharField(max_length=200)
    cameraPermitted = models.CharField(max_length=20)
    recordDate = models.DateTimeField()


class ConsentPageResults(models.Model):
    """

    """
    selectedAnswer = models.CharField(max_length=200)
    width = models.IntegerField()
    height = models.IntegerField()
    durationPage = models.FloatField(null=True, blank=True)
    recordDate = models.DateTimeField()
