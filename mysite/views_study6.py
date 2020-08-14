from django.shortcuts import render_to_response, render, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader, RequestContext
from django.template.loader import render_to_string
from datetime import *
import urllib
import hashlib, zlib
import cPickle as pickle
from django.utils import timezone
import json
import math
import random
from django.db.models import Count
from django.template.context_processors import csrf
from django.utils.safestring import mark_safe
from models import Users, Response, ImagePool, Results, MessagePool, InstructionPageResults, Score, ConsentPageResults, CameraPermission

import collections

my_secret = "AQKLYUFGPOAQQVBN2)?GHsasqqjjhh"
RISK_GROUP = "HIGH"

# 05-05-20 07:50 AM
def register_user(request):

    error = ''
    if request.method == "POST":
        if not request.POST.get('mTurkId', ''):
            error = 'Enter a valid mTurkId.'

        mTurkId =  request.POST.get('mTurkId')
        existing = Users.objects.filter(mTurkId = mTurkId)

        if existing.count() == 1:
            error = 'This MturkId(' + mTurkId + ') is already in the database. You can only participate once!'
        else:
            groupId = assignGroupNumber()
            #groupId = assignGroupNumber2()
            u = Users(mTurkId=mTurkId, groupId=groupId, groupName=getGroupName(groupId), dateParticipated=timezone.now())
            u.save()
            hash, enc = encode_data([mTurkId])

            return HttpResponseRedirect('/instruction/%s/%s/%s/' % (hash, enc,"1")) # start with round-1
    c = RequestContext(request,{'error':error})
    c.update(csrf(request))
    return render_to_response('study6/register.html', c)


# 05-05-20 07:15 AM
def viewInfoSheetPage(request):
    #return HttpResponse("Thank you for your interest in participating in this study. However, we are not currently recruiting any participants for this study, please check back later!")
    context = {}

    if RISK_GROUP == "HIGH":
        template = 'study6/infoSheet-HIGH.html'
    else:
        template = 'study6/infoSheet-LOW.html'
    return render(request, template, context)


# 05-05-20 11:20 AM
def viewInstructionPage(request, hash, enc, round):

    mTurkId = decode_data(hash, enc)[0]
    groupId = getGroupIdFromMTurkId(mTurkId)

    groupId = int(groupId)

    gameplayImg = "automation-game.png"
    manualGif = "manual-automation-gameplay.mp4"
    automationGif = "partner-automation.mp4"
    allocationGif = "automation-allocation.mp4"

    partner = "ATD"
    if groupId % 2 == 0:
        partner = "HUMAN"

    risk = "High"
    if 1 <= groupId <= 2 or 5 <= groupId <= 6:
        risk = "Low"


    if partner == "HUMAN":
        gameplayImg = "human-game.png"
        manualGif = "manual-human-gameplay.mp4"
        automationGif = "partner-human.mp4"
        allocationGif = "human-allocation.mp4"


    context = {
        'hash': hash,
        'enc': enc,
        'round': round,
        'gameplayImg': gameplayImg,
        'automationGif': automationGif,
        'manualGif': manualGif,
        'allocationGif': allocationGif,
        'partner': partner,
        'risk': risk,
        }
    template = 'study6/instructions.html'
    return render(request, template, context)


# 05-30-20 05:00 AM
def viewInstructionRiskPage(request, hash, enc, round):
    mTurkId = decode_data(hash, enc)[0]
    groupId = getGroupIdFromMTurkId(mTurkId)

    groupId = int(groupId)

    partner = 'ATD'
    partner_msg = 'You have been paired with an <strong>automated target detection system</strong> who is going to act as your partner in this game.'
    if groupId % 2 == 0:
        partner = 'HUMAN'
        partner_msg = 'You have been paired with another <strong>Mechanical Turk worker</strong> who is going to act as your partner in this game.'
    partner_msg = mark_safe(partner_msg)

    risk = 'High'
    if 1 <= groupId <= 2 or 5 <= groupId <= 6:
        risk = 'Low'

    if risk == 'Low':
        if partner == 'HUMAN':
            risk_msg = '<strong>Each member of your team can earn $5.00 based on your total score. However, if you are not one of the top 50% scoring teams in your game condition, you will receive $4.00. You have $1.00 at stake.</strong>'
        else:
            risk_msg = '<strong>You can earn $5.00 based on your total score. However, if you are not one of the top 50% scoring teams in your game condition, you will receive $4.00. You have $1.00 at stake.</strong>'
    else:
        if partner == 'HUMAN':
            risk_msg = '<strong>Each member of your team can earn $5.00 based on your total score. However, if you are not one of the top 50% scoring teams in your game condition, you will receive $2.00. You have $3.00 at stake.</strong>'
        else:
            risk_msg = '<strong>You can earn $5.00 based on your total score. However, if you are not one of the top 50% scoring teams in your game condition, you will receive $2.00. You have $3.00 at stake.</strong>'

    risk_msg = mark_safe(risk_msg)

    context = {
        'hash': hash,
        'enc': enc,
        'round': round,
        'partner': partner,
        'partner_msg': partner_msg,
        'risk': risk,
        'risk_msg': risk_msg,
        }
    template = 'study6/instructions_risk.html'
    return render(request, template, context)


# 05-05-20 11:00 AM
def viewConsentNotGivenMessage(request):
    """
    Called when user chooses not to participate.
    """
    context = {}
    template = 'study6/consent_not_given.html'
    return render(request, template, context)



# 05-05-20 02:10 PM
def viewInitialMessage(request, hash, enc, round):

    mTurkId = decode_data(hash,enc)[0]
    groupId = getGroupIdFromMTurkId(mTurkId)

    groupId = int(groupId)

    message = "Welcome! These messages will be used to communicate with you about your partner's performance."

    risk = "High"
    if 1 <= groupId <= 2 or 5 <= groupId <= 6:
        risk = "Low"

    partner = "ATD"
    allocationGif = ""
    if groupId % 2 == 0:
        partner = "HUMAN"
        allocationGif = "teammate5.mp4"

    context = {
        'hash': hash,
        'enc': enc,
        'nextRound': round,
        'messageTxt': message,
        'risk': risk,
        'partner': partner,
        'allocationGif': allocationGif,
        'allocationStatement': getAllocationStatement(groupId),
        }

    template = 'study6/initalMessage.html'

    return render(request, template, context)


# 05-07-20 05:00 AM
def begin(request, hash, enc, round):

    maxRound = 6
    mTurkId = decode_data(hash, enc)[0]
    groupId = getGroupIdFromMTurkId(mTurkId)

    # TODO identify/check true round number

    numImgToManual = 0
    numImgToAuto = 0
    request.session['startTimeRound' + round] = str(datetime.now())


    if 1 <= int(round) <= maxRound:
        # get the allocation number from the request
        if request.method == 'POST':

            agentGif = ""

            if int(groupId) % 2 == 0:
                agentGif = "teammate{0}.mp4".format(round)


            partner = "ATD"
            if int(groupId) % 2 == 0:
                partner = "HUMAN"

            numImgToAuto = 0
            numImgToManual = 0
            if 1 <= int(round) < maxRound:
                numImgToAuto =  request.POST.get('allocationToAutomation')
                numImgToManual = 20 - int(numImgToAuto)

            # save info from the results page into the DB
            #TODO get time zone offset datetime.strptime(request.POST.get('recordDate'),'%Y-%m-%d %H:%M:%S')
            durationResults = 0
            durationResultPage = 0
            durationGamePage = 0
            if 2 <= int(round) <= maxRound:
                durationResults = request.POST.get('durationResults')
                durationResultPage = request.POST.get('durationResultPage')
                durationGamePage = request.session['durationRound' + str(int(round)-1)]

            Results.objects.create(
                mTurkId=mTurkId,
                groupId=groupId,
                roundNumber=round,
                durationMessage=request.POST.get('durationMessage'),
                numImgToManual=numImgToManual, numImgToAuto=numImgToAuto,
                durationAllocation=request.POST.get('durationAllocation'),
                durationResults=durationResults,
                durationResultPage=durationResultPage,
                durationGamePage=durationGamePage,
                recordDate=datetime.now()
                )

            if int(round) == maxRound:
                # launch the survey page
                context = {"groupId": groupId}
                template = 'study6/survey.html'
                return render(request, template, context)
        else:
            return HttpResponse("Unfortunately, you will not be able to complete the study since the page was refreshed.")

    else:
        return HttpResponse("Invalid round number!")

    context = {
        'hash': hash,
        'enc': enc,
        'round': round,
        'numImgToManual': numImgToManual,
        'numImgToAuto': numImgToAuto,
        'numImgNotProcessed': getAutomationCorrectness(int(numImgToAuto), int(groupId), int(round))[1],
        'partner': partner,
        'agentGif': agentGif,
        'autoSpeed': getAvgAutomationTime(1, int(round))*1000,
        }
    template = 'study6/game.html'
    return render(request, template, context)


# 05-07-20 02:40 PM
# REVISION REQUIRED
@csrf_exempt
def recordAnswers(request, hash, enc, round):
    """
    Internally called using ajax from game.html. No template associated.
    It calls 'resultsAndMessages.html' -> next
    """

    mTurkId = decode_data(hash, enc)[0]
    groupId = getGroupIdFromMTurkId(mTurkId)

    if request.method == 'POST':
        json_data = request.POST['Data']
        json_data = json.loads(json_data)

        numImgCorrectManual = 0
        numImgIncorrectManual = 0
        avgTimeManual = 0
        numImgAllocatedAuto = 0
        numImgAllocatedManual = 0

        try:

            numImgAllocatedAuto = json_data['numImgToAuto']
            numImgAllocatedManual = json_data['numImgToManual']
            finishTimeManual = json_data['finishTimeManual']
            pageDuration = json_data['pageDuration']  # in seconds
            trajectory = json_data['trajectory']

            for item in json_data['results']:
                imageObj = ImagePool.objects.get(imageId=item['imageId'])
                userAnswer = ''
                if item['answer'] == 'yes':
                    userAnswer = 'enemy'
                elif item['answer'] == 'no':
                    userAnswer = 'friendly'
                if imageObj.enemyOrFriendly == userAnswer:
                    correctOrNot = 1
                    numImgCorrectManual += 1
                else:
                    correctOrNot = 0
                    numImgIncorrectManual += 1

                Response.objects.create(mTurkId=mTurkId,
                                        groupId=groupId,
                                        roundNumber=round,
                                        imageId=item['imageId'],
                                        countZoomIn=item['countZoomIn'],
                                        countZoomOut=item['countZoomOut'],
                                        answer=item['answer'],
                                        correctOrNot=correctOrNot,
                                        durationToAnswer=item['durationToAnswer'],
                                        responseDate=item['responseDate'])
        except KeyError:
            return HttpResponseServerError("Malformed data!")

        # Set durationRound time
        durationGamePage = (datetime.now() - datetime.strptime(request.session['startTimeRound' + round], '%Y-%m-%d %H:%M:%S.%f')).seconds
        request.session['durationRound' + round] = durationGamePage

        if not finishTimeManual:
            finishTimeManual = 0

        if numImgAllocatedManual > 0:
            avgTimeManual = float(finishTimeManual) / numImgAllocatedManual

        numImgCorrectAuto, numImgIncorrectAuto = getAutomationCorrectness(numImgAllocatedAuto, groupId, int(round))

        avgTimeAuto = getAvgAutomationTime(numImgAllocatedAuto, int(round))
        totalTimeAuto = numImgAllocatedAuto * avgTimeAuto

        # Automation may not be able to finish in 120 seconds
        if totalTimeAuto > 120:
            totalTimeAuto = min(totalTimeAuto, 120)
            autoCheckedImages = math.floor(120 / avgTimeAuto)
            numImgCorrectAuto = math.ceil(autoCheckedImages * getGroupReliability(int(groupId), int(round)))
            numImgIncorrectAuto = numImgAllocatedAuto - numImgCorrectAuto

        percentCorrect = float(numImgCorrectManual + numImgCorrectAuto)/float(numImgAllocatedManual + numImgAllocatedAuto)

        accScore, timeScore, totalScore = scoreCalculation(pageDuration, percentCorrect, int(groupId))

        messageObj = MessagePool.objects.get(groupId=groupId)
        message = messageObj.message

        if numImgIncorrectAuto == 1:
            message = message.replace("X images", "1 image")
        else:
            message = message.replace("X", str(int(numImgIncorrectAuto)))

        if numImgAllocatedAuto == 1:
            message = message.replace("Y images", "1 image")
        else:
            message = message.replace("Y", str(int(numImgAllocatedAuto)))

        if numImgAllocatedAuto == 0:
            message = "No Images were allocated to the partner."

        allocationGif = ""
        partner = "ATD"
        if int(groupId) % 2 == 0:
            partner = "HUMAN"
            allocationGif = "teammate{0}.mp4".format(6-int(round))

        #return HttpResponse("rawScore=%s, noiseScore=%s, totalScore=%s, groupId = %s"%(rawScore, noiseScore, totalScore, groupId))

        context = {'hash': hash,
                    'enc': enc,
                    'nextRound': int(round) + 1,
                    'numImgAllocatedManual': numImgAllocatedManual,
                    'numImgAllocatedAuto': numImgAllocatedAuto,
                    'numImgCorrectManual': numImgCorrectManual,
                    'numImgCorrectAuto': numImgCorrectAuto,
                    'numImgIncorrectManual': numImgIncorrectManual,
                    'numImgIncorrectAuto': numImgIncorrectAuto,
                    'totalTimeManual': finishTimeManual,
                    'totalTimeAuto': totalTimeAuto,
                    'avgTimeManual': avgTimeManual,
                    'avgTimeAuto': avgTimeAuto,
                    'totalImgAllocated': numImgAllocatedManual + numImgAllocatedAuto,
                    'totalCorrect': numImgCorrectManual + numImgCorrectAuto,
                    'totalIncorrect': numImgIncorrectManual + numImgIncorrectAuto,
                    'totalTime': max(finishTimeManual, totalTimeAuto),
                    'totalTimeAvg': max(avgTimeManual, avgTimeAuto),
                    'totalScore': totalScore,
                    'prevRound': round,
                    'message': message,
                    'allocationStatement': getAllocationStatement(int(groupId)),
                    'partner':partner,
                    'allocationGif': allocationGif,
                    }

        # return HttpResponse("accScore=%s, timeScore=%s, totalScore=%s, avgScore = %s, groupId = %s, allocationStatement = %s"%(accScore, timeScore, totalScore, avgScore, groupId, allocationStatement))
        Score.objects.create(mTurkId=mTurkId,
                            groupId=groupId,
                            groupName=getGroupName(groupId),
                            roundNumber=round,
                            numImgAllocatedManual=numImgAllocatedManual,
                            numImgAllocatedAuto=numImgAllocatedAuto,
                            numImgCorrectManual=numImgCorrectManual,
                            numImgCorrectAuto=numImgCorrectAuto,
                            numImgIncorrectManual=numImgIncorrectManual,
                            numImgIncorrectAuto=numImgIncorrectAuto,
                            totalTime=pageDuration,
                            totalTimeManual=finishTimeManual,
                            totalTimeAuto=totalTimeAuto,
                            avgTimeManual=avgTimeManual,
                            avgTimeAuto=avgTimeAuto,
                            accScore=accScore,
                            timeScore=timeScore,
                            roundScore=totalScore,
                            trajectory=trajectory,
                            recordDate=datetime.now()
                            )

        template = 'study6/resultsAndMessages.html'
        return render(request, template, context)
    else:
        return HttpResponse("Something went wrong!")


# 05-07-20 10:10 AM
@csrf_exempt
def checkImageCorrectness(request):
    """
    Internally called using ajax from game-js.js. No template associated.
    """

    if request.method == 'POST':
        answer = request.POST['answer']
        imageId = request.POST['imageId']

        imageObj = ImagePool.objects.get(imageId=imageId)
        userAnswer = ''
        if answer == 'yes':
            userAnswer = 'enemy'
        elif answer == 'no':
            userAnswer = 'friendly'

        if imageObj.enemyOrFriendly == userAnswer:
            return HttpResponse("Correct")
        else:
            return HttpResponse("Incorrect")
    else:
        return HttpResponse("Request is not a post!")


# 05-05-20 01:45 PM
@csrf_exempt
def checkInstructionCorrectness(request):
    """
    Internally called using ajax. No template associated.
    """

    if request.method == 'POST':
        question1 = request.POST['question1']
        question2 = request.POST['question2']
        question3 = request.POST['question3']
        question4 = request.POST['question4']
        question5 = request.POST['question5']
        question6 = request.POST['question6']
        question7 = request.POST['question7']

        answer = {
            "question1": question1,
            "question2": question2,
            "question3": question3,
            "question4": question4,
            "question5": question5,
            "question6": question6,
            "question7": question7,
            }

        # TODO create database and then check
        mTurkId = decode_data(request.POST['hash'],request.POST['enc'])[0]
        groupId = getGroupIdFromMTurkId(mTurkId)

        # TODO check from database
        numberOfCorrect = 0
        if question1 == 'car4':
            numberOfCorrect += 1
        if question2 == 'car3':
            numberOfCorrect += 1
        if question3 == 'option3':
            numberOfCorrect += 1
        if question4 == 'option1':
            numberOfCorrect += 1
        if question5 == 'option2':
            numberOfCorrect += 1
        if question7 == 'option2':
            numberOfCorrect += 1

        InstructionPageResults.objects.create(
            mTurkId=mTurkId,
            groupId=groupId,
            numberOfAttempt=request.POST['numberOfAttempt'],
            selectedAnswer=json.dumps(answer),
            durationPage=request.POST['durationPage'],
            numberOfCorrect=numberOfCorrect,
            recordDate=datetime.now()
            )
        return HttpResponse(numberOfCorrect)
    else:
        return HttpResponse("Request is not a post!")


# 05-30-20 05:30 AM
@csrf_exempt
def checkInstructionRiskCorrectness(request):
    """
    Internally called using ajax. No template associated.
    """

    if request.method == 'POST':
        question1 = request.POST['question1']
        question2 = request.POST['question2']
        question3 = request.POST['question3']

        answer = {
            "question1": question1,
            "question2": question2,
            "question3": question3,
            }

        # TODO create database and then check
        mTurkId = decode_data(request.POST['hash'],request.POST['enc'])[0]
        groupId = int(getGroupIdFromMTurkId(mTurkId))

        partner = "ATD"
        if groupId % 2 == 0:
            partner = "HUMAN"

        risk = "High"
        if 1 <= groupId <= 2 or 5 <= groupId <= 6:
            risk = "Low"

        # TODO check from database
        numberOfCorrect = 0
        if question1 == partner:
            numberOfCorrect += 1

        if question2 == 'option4':
            numberOfCorrect += 1

        if risk == 'Low' and question3 == 'option1':
            numberOfCorrect += 1
        elif risk == 'High' and question3 == 'option3':
            numberOfCorrect += 1


        InstructionPageResults.objects.create(
            mTurkId=mTurkId,
            groupId=groupId,
            numberOfAttempt=request.POST['numberOfAttempt'],
            selectedAnswer=json.dumps(answer),
            durationPage=request.POST['durationPage'],
            numberOfCorrect=numberOfCorrect,
            recordDate=datetime.now()
            )

        return HttpResponse(numberOfCorrect)
    else:
        return HttpResponse("Request is not a post!")


# 08-13-20 09:20 PM
@csrf_exempt
def recordCameraPermission(request):
    """
    Internally called using ajax. No template associated.
    """

    if request.method == 'POST':
        yes_no = request.POST['yes_no']

        # TODO create database and then check
        mTurkId = decode_data(request.POST['hash'],request.POST['enc'])[0]
        groupId = int(getGroupIdFromMTurkId(mTurkId))

        CameraPermission.objects.create(
            mTurkId=mTurkId,
            groupId=groupId,
            cameraPermitted=yes_no,
            recordDate=datetime.now()
            )

        return HttpResponse('ok')
    else:
        return HttpResponse("Request is not a post!")

# 05-05-20 07:50 AM
@csrf_exempt
def checkConsent(request):
    """
    Internally called using ajax. No template associated.
    """

    if request.method == 'POST':
        question1 = request.POST['question1']
        width = request.POST['width']
        height = request.POST['height']

        answer = {"question1": question1}

        result = ''
        if question1 == 'option1':
            result = 'ok'

        ConsentPageResults.objects.create(
            selectedAnswer = json.dumps(answer),
            width = width,
            height = height,
            durationPage = request.POST['durationPage'],
            recordDate = datetime.now()
            )
        return HttpResponse(result)
    else:
        return HttpResponse("Request is not a post!")


# CREATED on 07-12-20 10:01 PM
def scoreCalculation(pageDuration, percentCorrect, groupId):

    maxTime = 120.0
    minTime = 0

    timeCoeff = 100.0
    timeExp = 1.0

    # If duration to answer is greater than maxTime, timeScore will be 0.
    timeScore = 0
    if maxTime > pageDuration:
        timeNumerator = pageDuration - minTime
        timeDenominator = maxTime - minTime
        timeDiv = timeNumerator / timeDenominator
        timeDiv = 1 - timeDiv
        timeScore = timeCoeff*pow(timeDiv,timeExp)
        if timeScore > 100:
            timeScore = 100


    accCoeff = 100.0
    accExp = 1.25

    accScore = accCoeff*pow(percentCorrect, accExp)

    totalScore = (timeScore + accScore)/2
    return accScore, timeScore, totalScore



# NOT USED
def scoreCalculation2(numImgAllocatedAuto, groupId):
    pass

    # TED CHANGES

    """
    lowIdeal = 5.0
    highIdeal = 15.0
    maxScore = 90.0
    score = 0

    # Low reliablity
    if 1 <= groupId <= 4:
        score = maxScore*(1 - abs(numImgAllocatedAuto - lowIdeal)/20)

    # High reliability
    elif 5 <= groupId <= 8 :
        score = maxScore*(1 - abs(numImgAllocatedAuto - highIdeal)/20)

    # Add noise
    noiseInt = random.randint(0, 300)
    noise = (noiseInt - 150)/100

    totalScore = score + noise

    return score, noise, totalScore
    """



# 05-07-20 03:10 PM
def getAutomationCorrectness(numImgAllocatedAuto, groupId, round):
    numImgCorrectAuto = math.floor(int(numImgAllocatedAuto) * getGroupReliability(int(groupId), int(round)))
    numImgIncorrectAuto = int(numImgAllocatedAuto) - numImgCorrectAuto
    return numImgCorrectAuto, numImgIncorrectAuto


# 07-12-20 08:46 PM
def getAvgAutomationTime(numImgAllocatedAuto, round):
    #speeds = [9.1, 7.5, 6.9, 6.7, 6.5]
    noise = random.randrange(0, 11) / 10.0  # a random number [0.0, 1.0]
    noise -= 0.50                           # a random number [-0.5, 0.5]

    speed = 5
    speed += noise

    if numImgAllocatedAuto == 0:
        return 0

    return speed


# 05-07-20 05:00 AM
def getGroupReliability(groupId, round):

    #shift = (random.randrange(11) - 5) / 100.0
    noises = [0.04, -0.05, 0.01, -0.04, 0.04]
    shift = noises[int(round) - 1]

    highReliability = 0.9 + shift
    lowReliability = 0.6 + shift
    messageObj = MessagePool.objects.get(groupId=groupId)
    groupReliability = messageObj.groupReliability

    if groupReliability == "low":
        return lowReliability
    else:
        return highReliability


# 05-07-20 02:40 PM
def getGroupName(groupId):
    messageObj = MessagePool.objects.get(groupId=groupId)
    return messageObj.groupName


# 05-05-20 02:50 PM
def getAllocationStatement(groupId):
    """
    Message shown in the allocation panel.
    """
    allocationStatement = "Number of images to allocate to your partner for Round"

    return allocationStatement



# 05-05-20 10:20 AM
def addImagesToDb(request):
    """
    I need to call this function manually by going to url: .../add_images/
    to enter the images into database everytime I reset the database.
    """

    # TODO: write a script to save images to DB
    results = []
    imageFileName = ""
    for i in xrange(1, 21):
        if i <= 10:
            enemyOrFriendly = 'friendly'
        else:
            enemyOrFriendly = 'enemy'

        imageFileName = 'car' + str(i) + '.jpg'
        ImagePool.objects.create(imageFileName = imageFileName, imageId = i,
            enemyOrFriendly = enemyOrFriendly, countUsage = 0)
        results.append(imageFileName)

    return HttpResponse("results = %s" %results)


# 05-05-20 09:20 AM
def addMessagesToDb(request):
    """
    I need to call this function manually by going to url: .../add_messages/
    to enter the messages (more likely group info) into database everytime I reset the database.
    """
    # TODO: write a script, improve it, check unique!

    msg = "X images out of the Y images assigned to your partner were counted as misidentifications."

    Message = collections.namedtuple("Message", ["groupId", "groupName", "groupReliability", "message"])

    low_rel_low_risk_machine    = Message(groupId=1, groupName="low_rel_low_risk_machine", groupReliability="low", message=msg)
    low_rel_low_risk_human      = Message(groupId=2, groupName="low_rel_low_risk_human",   groupReliability="low", message=msg)

    low_rel_high_risk_machine   = Message(groupId=3, groupName="low_rel_high_risk_machine", groupReliability="low", message=msg)
    low_rel_high_risk_human     = Message(groupId=4, groupName="low_rel_high_risk_human",   groupReliability="low", message=msg)

    high_rel_low_risk_machine   = Message(groupId=5, groupName="high_rel_low_risk_machine", groupReliability="high", message=msg)
    high_rel_low_risk_human     = Message(groupId=6, groupName="high_rel_low_risk_human",   groupReliability="high", message=msg)

    high_rel_high_risk_machine  = Message(groupId=7, groupName="high_rel_high_risk_machine", groupReliability="high", message=msg)
    high_rel_high_risk_human    = Message(groupId=8, groupName="high_rel_high_risk_human",   groupReliability="high", message=msg)

    Messages = [
        low_rel_low_risk_machine, low_rel_low_risk_human,
        low_rel_high_risk_machine, low_rel_high_risk_human,
        high_rel_low_risk_machine, high_rel_low_risk_human,
        high_rel_high_risk_machine, high_rel_high_risk_human,
        ]


    for msg in Messages:
        MessagePool.objects.create(groupId=msg.groupId, groupName=msg.groupName, groupReliability=msg.groupReliability, message=msg.message)


    return HttpResponse(str(len(Messages)) + " messages assigned to " +  str(len(Messages)) + " groups")





#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
############################################# Some utility methods ####################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


# 05-05-20 01:50 PM
def getGroupIdFromMTurkId(mTurkId):
    userObj = Users.objects.get(mTurkId=mTurkId)
    return userObj.groupId


# 05-05-20 07:50 AM
'''
Low  Reliabilty Low  Risk Automation = 1
Low  Reliabilty Low  Risk Human      = 2
Low  Reliabilty High Risk Automation = 3
Low  Reliabilty High Risk Human      = 4
High Reliabilty Low  Risk Automation = 5
High Reliabilty Low  Risk Human      = 6
High Reliabilty High Risk Automation = 7
High Reliabilty High Risk Human      = 8

Low  Risk = {0: 1, 1: 2, 2: 5, 3: 6,}
High Risk = {0: 3, 1: 4, 2: 7, 3: 8,}

'''
@csrf_exempt
def assignGroupNumber():
	# TODO: improve this method!
    """
    numberOfGroups = 8
    numberOfUsers = Users.objects.all().count()
    return (numberOfUsers % numberOfGroups) + 1
    """
    numberOfUsers = Users.objects.all().count()
    t = numberOfUsers % 4

    low_dict = {0: 1, 1: 2, 2: 5, 3: 6,}
    high_dict = {0: 3, 1: 4, 2: 7, 3: 8,}

    if RISK_GROUP == "HIGH":
        return high_dict[t]
    else:
        return low_dict[t]



@csrf_exempt
def assignGroupNumber2():

	# TODO: improve this method!!!

    count_actual = Users.objects.values('groupId').order_by('groupId').annotate(the_count=Count('groupId'))

    count_prev = [
            {'the_count': 41, 'groupId': '1'},
            {'the_count': 38, 'groupId': '2'},
            {'the_count': 38, 'groupId': '3'},
            {'the_count': 45, 'groupId': '4'},
            {'the_count': 41, 'groupId': '5'},
            {'the_count': 38, 'groupId': '6'},
            {'the_count': 38, 'groupId': '7'},
            {'the_count': 45, 'groupId': '8'},
    ]


    count_qualtrics = [
            {'the_count': 25, 'groupId': '1'},
            {'the_count': 29, 'groupId': '2'},
            {'the_count': 31, 'groupId': '3'},
            {'the_count': 25, 'groupId': '4'},
            {'the_count': 25, 'groupId': '5'},
            {'the_count': 29, 'groupId': '6'},
            {'the_count': 31, 'groupId': '7'},
            {'the_count': 25, 'groupId': '8'},
    ]
    count = []
    for actual in count_actual:
        for index, prev in enumerate(count_prev):
            if actual['groupId'] == prev['groupId']:
                diff = actual['the_count'] - prev['the_count']
                count.append({'the_count':(count_qualtrics[index]['the_count'] + diff),
                              'groupId': actual['groupId']})

    minGroupId = min(count, key = lambda x:x['the_count'])['groupId']
    return int(minGroupId)



def encode_data(data):
    """Turn `data` into a hash and an encoded string, suitable for use with `decode_data`."""
    text = zlib.compress(pickle.dumps(data, 0)).encode('base64').replace('\n', '')
    m = hashlib.md5(my_secret + text).hexdigest()[:12]
    return m, text.replace('/', '_')


def decode_data(hash, enc):
    """The inverse of `encode_data`."""
    text = urllib.unquote(enc.replace('_', '/'))
    m = hashlib.md5(my_secret + text).hexdigest()[:12]
    if m != hash:
        raise Exception("Bad hash!")
    data = pickle.loads(zlib.decompress(text.decode('base64')))
    return data


def page_not_found(request, template_name='study6/404.html'):
    t = loader.get_template("study6/404.html")
    return HttpResponseServerError(render_to_string('study6/404.html', context_instance=RequestContext(request)))


def server_error(request, template_name='study6/500.html'):
    t = loader.get_template("study6/500.html")
    return HttpResponseServerError(render_to_string('study6/500.html', context_instance=RequestContext(request)))

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
############################################# TEST ####################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def test(request):
    return HttpResponse("This is a test!")


def test2(request):

    # Clears the tables
    ###ConsentPageResults.objects.all().delete()
    Score.objects.all().delete()
    ###InstructionPageResults.objects.all().delete()
    ###Results.objects.all().delete()
    ###Response.objects.all().delete()
    ###Users.objects.all().delete()

    return HttpResponse("This is a test2!")

def test3(request):

    #return HttpResponse("This is test3!")
    #context = {"groupId": 1}
    #template = 'survey.html'
    #return render(request, template, context)
    return HttpResponse("This is test3!")

def test4(request):

    count_actual = Users.objects.values('groupId').order_by('groupId').annotate(the_count=Count('groupId'))

    count_prev = [
            {'the_count': 41, 'groupId': '1'},
            {'the_count': 38, 'groupId': '2'},
            {'the_count': 38, 'groupId': '3'},
            {'the_count': 45, 'groupId': '4'},
            {'the_count': 41, 'groupId': '5'},
            {'the_count': 38, 'groupId': '6'},
            {'the_count': 38, 'groupId': '7'},
            {'the_count': 45, 'groupId': '8'},
    ]


    count_qualtrics = [
            {'the_count': 25, 'groupId': '1'},
            {'the_count': 29, 'groupId': '2'},
            {'the_count': 31, 'groupId': '3'},
            {'the_count': 25, 'groupId': '4'},
            {'the_count': 25, 'groupId': '5'},
            {'the_count': 29, 'groupId': '6'},
            {'the_count': 31, 'groupId': '7'},
            {'the_count': 25, 'groupId': '8'},
    ]

    count = []
    for actual in count_actual:
        for index, prev in enumerate(count_prev):
            if actual['groupId'] == prev['groupId']:
                diff = actual['the_count'] - prev['the_count']
                count.append({'the_count':(count_qualtrics[index]['the_count'] + diff),
                              'groupId': actual['groupId']})

    minGroupId = min(count, key = lambda x:x['the_count'])['groupId']
    return HttpResponse("minGroupId = %s, count = %s" %(minGroupId, count))
    #return HttpResponse("This is test4!")
    #context = {"groupId": 9}
    #template = 'survey.html'
    #return render(request, template, context)
    return HttpResponse("This is test4!")

