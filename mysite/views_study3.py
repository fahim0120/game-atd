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
from django.db.models import Count
from django.utils import timezone
import settings
from django.template.context_processors import csrf
from models import Users, Response, ImagePool, Results, MessagePool, InstructionPageResults, Score, ConsentPageResults

my_secret = "AQKLYUFGPOAQQVBN2)?GHsasqqjjhh"


def register_user(request):

    error = ''
    if request.method == "POST":
        if not request.POST.get('mTurkId', ''):
            error = 'Enter a valid mTurkId.'

        mTurkId =  request.POST.get('mTurkId')
        existing = Users.objects.filter(mTurkId = mTurkId)
        #return HttpResponse("mTurkId=%s [mTurkId]=%s"%(mTurkId, [mTurkId]))

        if existing.count() == 1:
            error = 'This MturkId(' + mTurkId + ') is already in the database. You can only participate once!'
        else:
            groupId = assignGroupNumber()
            #return HttpResponse("groupId=%s"%groupId)datetime.datetime.now(tz=timezone.utc) # you can use this value
            u = Users(mTurkId= mTurkId, groupId = groupId, groupName = getGroupName(groupId), dateParticipated = timezone.now())
            u.save()
            #return render_to_response('game.html')
            hash, enc = encode_data([mTurkId])

            #return HttpResponseRedirect('/begin2/%s/%s/%s/' % (hash, enc,"1")) # start with round-1
            return HttpResponseRedirect('/instruction/%s/%s/%s/' % (hash, enc,"1")) # start with round-1
    c = RequestContext(request,{'error':error})
    c.update(csrf(request))
    return render_to_response('study3/register.html',c)


def viewInfoSheetPage(request):
    return HttpResponse("Thank you for your interest in participating in this study. However, we are not currently recruiting any participants for this study, please check back later!")
    context = {}
    template = 'study3/infoSheet.html'
    return render(request, template, context)

def viewInstructionPage(request, hash, enc, round):
    context = {'hash':hash,'enc':enc,'round':round}
    template = 'study3/instractions.html'
    return render(request, template,context)

def viewConsentNotGivenMessage(request):
    context = {}
    template = 'study3/consent_not_given.html'
    return render(request, template,context)


#Study-3
def viewInitialMessage(request, hash, enc, round):

    mTurkId = decode_data(hash,enc)[0]
    groupId = getGroupIdFromMTurkId(mTurkId)

    #print("groupId", groupId)
    groupId = int(groupId)
    #print("groupId", groupId)

    message = ""
    if 1 <= groupId <= 2 :
        message = "The automated system tries its best to ensure that no dangerous vehicle escapes. "\
				  "In order to avoid missing any dangerous vehicle, the automated system may misidentify "\
				  "some innocent vehicles as dangerous. This may cause misuse of limited resources to stop "\
				  "innocent vehicles. This may also cause inconvenience to innocent people."

    elif 3 <= groupId <= 4 :
        message = "The automated system tries its best to ensure that no dangerous vehicle escapes. "\
				  "In order to avoid missing any dangerous vehicle, the automated system may misidentify "\
				  "some innocent vehicles as dangerous. It has been found in the previous studies that you "\
				  "might experience frustration, anger, and anxiety that this may cause misuse of limited "\
				  "resources to stop innocent vehicles. You might also experience remorse and regret that "\
				  "misidentification may cause inconvenience to innocent people."

    context = {'hash':hash,'enc':enc,'round':round, 'message': message}
    template = 'study3/initalMessage.html'

    return render(request, template,context)



def begin(request, hash, enc, round):

    #return HttpResponse("hash = %s, enc = %s"%(hash, enc))

    maxRound = 5
    mTurkId = decode_data(hash,enc)[0]
    groupId = getGroupIdFromMTurkId(mTurkId)

    #return HttpResponse("hash = %s, enc = %s mTurkId = %s"%(hash, enc, mTurkId))

    # TODO identify/check true round number

    numImgToManual = 0
    numImgToAuto = 0
    request.session['startTimeRound' + round] = str(datetime.now())

    if round == "1":
        numImgToManual = 10
        numImgToAuto = 10

        #return HttpResponse("duration = %s, enc = %s"%(datetime.now() - request.session['startTimeRound' + round], enc))
    elif 1 < int(round) <= maxRound:
        #return HttpResponse("Round = %s" %round)

        # get the allocation number from the request
        if request.method == 'POST':
            numImgToAuto =  request.POST.get('allocationToAutomation')
            numImgToManual = request.POST.get('allocationToManual')

            #return HttpResponse("numImgToAuto = %s, numImgToManual = %s"%(numImgToAuto, numImgToManual))

            # save info from the results page into the DB
            #TODO get time zone offset datetime.strptime(request.POST.get('recordDate'),'%Y-%m-%d %H:%M:%S')
            Results.objects.create(mTurkId = mTurkId, groupId = groupId, roundNumber = round,
                durationResults = request.POST.get('durationResults'),numImgToAuto = numImgToAuto,
                durationMessage = request.POST.get('durationMessage'), numImgToManual = numImgToManual,
                durationAllocation = request.POST.get('durationAllocation'),
                durationResultPage = request.POST.get('durationResultPage'),
                durationGamePage = request.session['durationRound' + str(int(round)-1)],
                recordDate = datetime.now())

            if int(round) == maxRound:
                # launch the survey page
                context = {"groupId": groupId}
                template = 'study3/survey.html'
                return render(request, template,context)
        else:
            return HttpResponse("Unfortunately, you will not be able to complete the study since the page was refreshed.")

    else:
        return HttpResponse("Invalid round number!")


    #autoCorrectness = getAutomationCorrectness(numImgToAuto, groupId)[1]
    #return HttpResponse("numImgAllocatedAuto = %s, groupId=%s, autoCorrectness=%s" %(numImgToAuto, groupId, autoCorrectness))
    context = {'hash':hash,'enc':enc,'round':round, 'numImgToManual': numImgToManual, 'numImgToAuto' : numImgToAuto,
               'numImgNotProcessed': getAutomationCorrectness(int(numImgToAuto), int(groupId))[1]}
    template = 'study3/game.html'
    return render(request, template,context)


@csrf_exempt
def recordAnswers(request, hash, enc, round):

    #return HttpResponse("hash = %s, enc = %s, round = %s "%(hash, enc, round))

    mTurkId = decode_data(hash,enc)[0]
    #return HttpResponse("mTurkId = %s, groupId = %s "%(mTurkId, '0'))
    groupId = getGroupIdFromMTurkId(mTurkId)
    #return HttpResponse("mTurkId = %s, groupId = %s "%(mTurkId, groupId))
    if request.method == 'POST':
        json_data = request.POST['Data']
        json_data = json.loads(json_data)
        #print json_data
        #print json_data['results']

        numImgCorrectManual = 0
        numImgIncorrectManual = 0
        #totalTimeManual = 0
        avgTimeManual = 0
        numImgAllocatedAuto = 0
        numImgAllocatedManual = 0

        try:
            numImgAllocatedAuto = json_data['numImgToAuto']
            numImgAllocatedManual = json_data['numImgToManual']
            finishTimeManual = json_data['finishTimeManual']
            #print "finishTimeManual", finishTimeManual
            #finishTimeAuto = json_data['finishTimeAuto']
            pageDuration = json_data['pageDuration'] # in seconds
            trajectory = json_data['trajectory']
            #print "pageDuration", pageDuration
            #print "trajectory", trajectory
            #return HttpResponse("trajectory = %s, pageDuration = %s"%(trajectory, pageDuration))

            for item in json_data['results']:
                imageObj = ImagePool.objects.get(imageId = item['imageId'])
                userAnswer = ''
                if item['answer'] == 'yes':
                    userAnswer = 'enemy'
                elif  item['answer'] == 'no':
                    userAnswer = 'friendly'
                if imageObj.enemyOrFriendly == userAnswer:
                    correctOrNot = 1
                    numImgCorrectManual += 1
                else:
                    correctOrNot = 0
                    numImgIncorrectManual += 1

                #totalTimeManual = totalTimeManual + item['durationToAnswer']

                Response.objects.create(mTurkId = mTurkId, groupId = groupId, roundNumber = round, imageId = item['imageId'],
                    countZoomIn = item['countZoomIn'], countZoomOut = item['countZoomOut'], answer = item['answer'],
                    correctOrNot = correctOrNot, durationToAnswer = item['durationToAnswer'],
                    responseDate = item['responseDate'])

        except KeyError:
            return HttpResponseServerError("Malformed data!")


        # Set durationRound time
        durationGamePage = (datetime.now() - datetime.strptime(request.session['startTimeRound' + round], '%Y-%m-%d %H:%M:%S.%f')).seconds
        request.session['durationRound' + round] = durationGamePage


        if not finishTimeManual:
            finishTimeManual= 0
        if numImgAllocatedManual > 0:
            avgTimeManual = float(finishTimeManual)/numImgAllocatedManual


        numImgCorrectAuto, numImgIncorrectAuto = getAutomationCorrectness(numImgAllocatedAuto, groupId)

        #return HttpResponse("numImgAllocatedAuto = %s, numImgCorrectAuto = %s, numImgIncorrectAuto = %s groupId=%s"%
        #                    (numImgAllocatedAuto, numImgCorrectAuto, numImgIncorrectAuto, groupId))


        avgTimeAuto = getAvgAutomationTime(numImgAllocatedAuto)
        totalTimeAuto = numImgAllocatedAuto * avgTimeAuto

        #return HttpResponse("round = %s, numImgAllocatedManual = %s, numImgAllocatedAuto = %s "%(round, numImgAllocatedManual, numImgAllocatedAuto))

        accScore, timeScore, totalScore, avgScore = scoreCalculation(pageDuration,
            float(numImgCorrectManual + numImgCorrectAuto)/float(numImgAllocatedManual + numImgAllocatedAuto))


        messageObj = MessagePool.objects.get(groupId = groupId)
        message = messageObj.message

        if numImgIncorrectAuto == 1:
            # Study-1
            #message = message.replace("images allocated", "image allocated")
            message = message.replace("These images were", "This image was")
            message = message.replace("as misidentifications", "as a misidentification")
            message = message.replace("There were", "There was")
            message = message.replace("X innocent vehicles", "X innocent vehicle")



            # Study-2
            message = message.replace("were counted", "was counted")
            message = message.replace("those images", "that image")

        message = message.replace("X", str(int(numImgIncorrectAuto)))

        if numImgAllocatedAuto == 0:
            message = "The ATD system was not used!"


        context = {'hash':hash,'enc':enc,'nextRound':int(round) + 1, 'numImgAllocatedManual': numImgAllocatedManual,
                    'numImgAllocatedAuto':numImgAllocatedAuto,'numImgCorrectManual':numImgCorrectManual,
                    'numImgCorrectAuto': numImgCorrectAuto, 'numImgIncorrectManual':numImgIncorrectManual,
                    'numImgIncorrectAuto': numImgIncorrectAuto, 'totalTimeManual': finishTimeManual,
                    'totalTimeAuto': totalTimeAuto, 'avgTimeManual': avgTimeManual,'avgTimeAuto': avgTimeAuto,
                    'totalImgAllocated' :numImgAllocatedManual + numImgAllocatedAuto,
                    'totalCorrect' : numImgCorrectManual + numImgCorrectAuto,
                    'totalIncorrect' : numImgIncorrectManual + numImgIncorrectAuto,
                    'totalTime': max(finishTimeManual, totalTimeAuto),
                    'totalTimeAvg' : max(avgTimeManual, avgTimeAuto),
                    'accScore': accScore, 'timeScore': timeScore, 'totalScore': totalScore,'avgScore': avgScore,
                    'prevRound':round, 'message': message}


        Score.objects.create(mTurkId = mTurkId, groupId = groupId, groupName = getGroupName(groupId), roundNumber = round,
            numImgAllocatedManual = numImgAllocatedManual, numImgAllocatedAuto = numImgAllocatedAuto,
            numImgCorrectManual = numImgCorrectManual, numImgCorrectAuto = numImgCorrectAuto,
            numImgIncorrectManual = numImgIncorrectManual, numImgIncorrectAuto = numImgIncorrectAuto,
            totalTime = pageDuration, totalTimeManual = finishTimeManual, totalTimeAuto = totalTimeAuto,
            avgTimeManual = avgTimeManual, avgTimeAuto = avgTimeAuto, accScore = accScore,
            timeScore = timeScore, roundScore = totalScore, trajectory = trajectory, recordDate = datetime.now())


        template = 'study3/resultsAndMessages.html'
        return render(request, template,context)
        #return HttpResponse("Success")
    else:
        return HttpResponse("Something went wrong!")


@csrf_exempt
def checkImageCorrectness(request):

    if request.method == 'POST':
        answer = request.POST['answer']
        imageId = request.POST['imageId']
        #return HttpResponse("answer=%s, imageId=%s"%(answer, imageId))

        imageObj = ImagePool.objects.get(imageId = imageId)
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


@csrf_exempt
def checkInstructionCorrectness(request):

    if request.method == 'POST':
        question1 = request.POST['question1']
        question2 = request.POST['question2']
        question3 = request.POST['question3']
        question4 = request.POST['question4']
        question5 = request.POST['question5']
        question6 = request.POST['question6']
        question7 = request.POST['question7']
        question8 = request.POST['question8']

        #print question1, question2, question3, question4, question5, question6, question7
        answer = {"question1": question1, "question2": question2, "question3": question3,
                "question4": question4, "question5":question5, "question6":question6,
                "question7":question7, "question8":question8}
        #print "answer:", answer
        #print(json.dumps(answer))
        #return HttpResponse("question1 = %s, question2 = %s, question3 = %s,"
        #                    " question4 = %s, question5 = %s "%(question1, question2, question3, question4, question5))


        # TODO create database and then check

        mTurkId = decode_data(request.POST['hash'],request.POST['enc'])[0]
        groupId = getGroupIdFromMTurkId(mTurkId)
        #print "groupId:", groupId
        #print "numberOfAttempt: ", request.POST['numberOfAttempt']

        # TODO check from database
        numberOfCorrect = 0
        if question1 == 'car4':
            numberOfCorrect += 1
        if question2 == 'car3':
            numberOfCorrect += 1
        if question3 == 'option3':
            numberOfCorrect += 1
        if question4 == 'option2':
            numberOfCorrect += 1
        if question5 == 'option1':
            numberOfCorrect += 1
        if question6 == 'option2':
            numberOfCorrect += 1
        if question8 == 'option2':
            numberOfCorrect += 1


        InstructionPageResults.objects.create(mTurkId = mTurkId, groupId = groupId,
            numberOfAttempt = request.POST['numberOfAttempt'], selectedAnswer = json.dumps(answer),
            durationPage = request.POST['durationPage'], numberOfCorrect = numberOfCorrect, recordDate = datetime.now())

        return HttpResponse(numberOfCorrect)
    else:
        return HttpResponse("Request is not a post!")


@csrf_exempt
def checkConsent(request):

    if request.method == 'POST':
        question1 = request.POST['question1']
        width = request.POST['width']
        height = request.POST['height']

        #print question1
        #print "width:", width
        #print "height:", height
        answer = {"question1": question1}
        #print "answer:", answer
        #print(json.dumps(answer))


        # TODO create database and then check

        #mTurkId = decode_data(request.POST['hash'],request.POST['enc'])[0]
        #print "mTurkId:", mTurkId
        #groupId = getGroupIdFromMTurkId(mTurkId)
        #print "groupId:", groupId


        result = ''
        if question1 == 'option1':
            result = 'ok'

        ConsentPageResults.objects.create(selectedAnswer = json.dumps(answer), width = width, height = height,
            durationPage = request.POST['durationPage'], recordDate = datetime.now())
        return HttpResponse(result)
    else:
        return HttpResponse("Request is not a post!")

def scoreCalculation(pageDuration, percentCorrect):

    #avgManTime = 6.0
    #avgAutoTime = 4.0

    maxTime = 120.0 #
    minTime = 0

    timeCoeff = 100.0
    timeExp = 1.0

    #print "totalTimeManual", totalTimeManual
    #print "totalTimeAuto", totalTimeAuto
    #maxDuration = max(totalTimeManual, totalTimeAuto)

    # If duration to Answer is greater than maxTime, timeScore will be 0.
    timeScore = 0
    if maxTime > pageDuration:
        timeNumerator = pageDuration - minTime
        timeDenominator = maxTime - minTime
        timeDiv = timeNumerator / timeDenominator
        timeDiv = 1 - timeDiv
        timeScore = timeCoeff*pow(timeDiv,timeExp)
        if timeScore > 100:
            timeScore = 100

    #print "timeScore", timeScore

    accCoeff = 100.0
    accExp = 1.25

    accScore = accCoeff*pow(percentCorrect, accExp)

    #print accScore
    avgScore = (timeScore + accScore)/2
    totalScore = timeScore + accScore
    #print "Total Score: ", totalScore
    return accScore, timeScore, totalScore, avgScore

def getAutomationCorrectness(numImgAllocatedAuto, groupId):
    #return HttpResponse("numImgAllocatedAuto = %s, groupId=%s " %(numImgAllocatedAuto, groupId))
    #print numImgAllocatedAuto, type(numImgAllocatedAuto)
    #print groupId, type(groupId)
    #print int(numImgAllocatedAuto) * int(groupId)
    numImgCorrectAuto = math.floor(int(numImgAllocatedAuto) * getGroupReliability(int(groupId)))
    numImgIncorrectAuto = int(numImgAllocatedAuto) - numImgCorrectAuto
    return numImgCorrectAuto, numImgIncorrectAuto


def getAvgAutomationTime(numImgAllocatedAuto):
    if numImgAllocatedAuto == 0:
        return 0
    automationTime = 3.1
    return automationTime


def getGroupReliability(groupId):
    highReliability = 0.9
    lowReliability = 0.6
    messageObj = MessagePool.objects.get(groupId = groupId)
    groupReliability = messageObj.groupReliability

    if groupReliability == "low":
        return lowReliability
    else:
        return highReliability


def getGroupName(groupId):
    messageObj = MessagePool.objects.get(groupId = groupId)
    return messageObj.groupName

def addImagesToDb(request):
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


#Study-3
def addMessagesToDb(request):
    # TODO: write a script, improve it, check unique!

    groupId = 0

    message = "The ATD system misidentified X innocent vehicles as dangerous."


    # Group 1 - 2
    groupId += 1
    MessagePool.objects.create(groupId = groupId, groupName = "lowReliability-noInoculation",
        groupReliability = "low", message = message)
    groupId += 1
    MessagePool.objects.create(groupId = groupId, groupName = "lowReliability-noInoculation",
        groupReliability = "low", message = message)


    # Group 3 - 4
    groupId += 1
    MessagePool.objects.create(groupId = groupId, groupName = "highReliability-inoculation",
        groupReliability = "high", message = message)
    groupId += 1
    MessagePool.objects.create(groupId = groupId, groupName = "highReliability-inoculation",
        groupReliability = "high", message = message)



    return HttpResponse(str(groupId) + " messages assigned to " +  str(groupId) + " groups")





#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
############################################# Some utility methods ####################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def getGroupIdFromMTurkId(mTurkId):
    userObj = Users.objects.get(mTurkId = mTurkId)
    return userObj.groupId

@csrf_exempt
def assignGroupNumber():
    # TODO: improve this method!
    numberOfGroups = 4
    numberOfUsers = Users.objects.all().count()
    return (numberOfUsers % numberOfGroups) +1

@csrf_exempt
def assignGroupNumber2():

    # TODO: improve this method!!!

    count_actual = Users.objects.values('groupId').order_by('groupId').annotate(the_count=Count('groupId'))


    count_prev = [
            {'the_count': 49, 'groupId': '1'},
            {'the_count': 44, 'groupId': '2'},
            {'the_count': 43, 'groupId': '3'},
            {'the_count': 44, 'groupId': '4'},
            {'the_count': 55, 'groupId': '5'},
            {'the_count': 48, 'groupId': '6'}
    ]


    count_qualtrics = [
            {'the_count': 30, 'groupId': '1'},
            {'the_count': 35, 'groupId': '2'},
            {'the_count': 35, 'groupId': '3'},
            {'the_count': 34, 'groupId': '4'},
            {'the_count': 31, 'groupId': '5'},
            {'the_count': 34, 'groupId': '6'}
    ]

    count = []
    for actual in count_actual:
        for index, prev in enumerate(count_prev):
            if actual['groupId'] == prev['groupId']:
                diff = actual['the_count'] - prev['the_count']
                count.append({'the_count':(count_qualtrics[index]['the_count'] + diff),
                              'groupId': actual['groupId']})
                #return HttpResponse("groupId=%s, diff = %s, a = %s" %(actual['groupId'], diff, a))

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

def page_not_found(request, template_name='404.html'):

    t = loader.get_template("study3/404.html") # Call 404.html template.
    return HttpResponseServerError(render_to_string('404.html', context_instance=RequestContext(request)))

def server_error(request, template_name='500.html'):

    t = loader.get_template("study3/500.html") # Call 500.html template.
    return HttpResponseServerError(render_to_string('500.html', context_instance=RequestContext(request)))



#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
############################################# TEST ####################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def test(request):

    #Users.objects.filter(mTurkId = 'A2BBDH8DZD77AU').delete()
    #return HttpResponse("MturkId has been removed!")

    #count = Users.objects.values('groupId').order_by('groupId').annotate(the_count=Count('groupId'))
    #minGroupId = min(count, key = lambda x:x['the_count'])['groupId']
    #return HttpResponse("minGroupId = %s" %(minGroupId))

    #context = {"groupId": 12}
    #template = 'survey.html'
    #return render(request, template, context)

    return HttpResponse("This is a test!")

    count_actual = Users.objects.values('groupId').order_by('groupId').annotate(the_count=Count('groupId'))

    count_prev = [
            {'the_count': 49, 'groupId': '1'},
            {'the_count': 44, 'groupId': '2'},
            {'the_count': 43, 'groupId': '3'},
            {'the_count': 44, 'groupId': '4'},
            {'the_count': 55, 'groupId': '5'},
            {'the_count': 48, 'groupId': '6'}
    ]


    count_qualtrics = [
            {'the_count': 30, 'groupId': '1'},
            {'the_count': 35, 'groupId': '2'},
            {'the_count': 35, 'groupId': '3'},
            {'the_count': 34, 'groupId': '4'},
            {'the_count': 31, 'groupId': '5'},
            {'the_count': 34, 'groupId': '6'}
    ]

    count = []
    for actual in count_actual:
        for index, prev in enumerate(count_prev):
            if actual['groupId'] == prev['groupId']:
                diff = actual['the_count'] - prev['the_count']
                count.append({'the_count':(count_qualtrics[index]['the_count'] + diff),
                              'groupId': actual['groupId']})
                #return HttpResponse("groupId=%s, diff = %s, a = %s" %(actual['groupId'], diff, a))

    minGroupId = min(count, key = lambda x:x['the_count'])['groupId']
    return HttpResponse("minGroupId = %s, count = %s" %(minGroupId, count))

    #Users.objects.filter(mTurkId = 'A15FXHC1CVNW31').delete()
    # Clears the tables
    #ConsentPageResults.objects.all().delete()
    #Score.objects.all().delete()
    #InstructionPageResults.objects.all().delete()
    #Results.objects.all().delete()
    #Response.objects.all().delete()
    #Users.objects.all().delete()
    #return HttpResponse("Tables have been cleared!")

    #return HttpResponse("Success!")
    #context = {}
    #template = 'test.html'
    #template = 'resultsAndMessages2_avatar.html'
    #return render(request, template,context)

def test2(request):
    return HttpResponse("This is test2!")

def test3(request):

    return HttpResponse("This is test3!")
    #context = {"groupId": 3}
    #template = 'survey.html'
    #return render(request, template, context)
    return HttpResponse("This is test3!")

def test4(request):

    return HttpResponse("This is test4!")
    #context = {"groupId": 3}
    #template = 'survey.html'
    #return render(request, template, context)
    return HttpResponse("This is test4!")




