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
from django.utils import timezone
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

        if existing.count() == 1:
            error = 'This MturkId(' + mTurkId + ') is already in the database. You can only participate once!'
        else:
            groupId = assignGroupNumber()
            #groupId = assignGroupNumber2()
            gifOrder = generateGifOrder()
            u = Users(mTurkId= mTurkId, groupId = groupId, groupName = getGroupName(groupId), dateParticipated = timezone.now(), gifOrder = gifOrder)
            u.save()
            hash, enc = encode_data([mTurkId])

            return HttpResponseRedirect('/instruction/%s/%s/%s/' % (hash, enc,"1")) # start with round-1
    c = RequestContext(request,{'error':error})
    c.update(csrf(request))
    return render_to_response('study5/register.html', c)


def viewInfoSheetPage(request):
    #return HttpResponse("Thank you for your interest in participating in this study. However, we are not currently recruiting any participants for this study, please check back later!")
    context = {}
    template = 'study5/infoSheet.html'
    return render(request, template, context)

def viewInstructionPage(request, hash, enc, round):

    mTurkId = decode_data(hash,enc)[0]
    groupId = getGroupIdFromMTurkId(mTurkId)

    groupId = int(groupId)

    # Study-5: gameplayGif, automationGif, allocationGif to be included, all based on agent condition
    gameplayImg = ""
    automationGif = ""
    manualGif = ""
    allocationGif = "allocation.gif"

    if groupId == 1 or groupId == 4: # Computer agent
        gameplayImg = "computer-game.PNG"
        manualGif = "computer-manual.gif"
        automationGif = "computer-auto.gif"
    elif groupId == 2 or groupId == 5: # Avatar agent
        gameplayImg = "avatar-game.PNG"
        manualGif = "avatar-manual.gif"
        automationGif = "avatar-auto.gif"
    elif groupId == 3 or groupId == 6: # Human agent
        gameplayImg = "human-game.PNG"
        manualGif = "human-manual.gif"
        automationGif = "human-auto.gif"


    context = {'hash':hash,'enc':enc,'round':round, 'gameplayImg': gameplayImg, 'automationGif': automationGif, 'manualGif': manualGif, 'allocationGif': allocationGif}
    template = 'study5/instractions.html'
    return render(request, template,context)

def viewConsentNotGivenMessage(request):
    context = {}
    template = 'study5/consent_not_given.html'
    return render(request, template,context)

def viewInitialMessage(request, hash, enc, round):

    mTurkId = decode_data(hash,enc)[0]
    groupId = getGroupIdFromMTurkId(mTurkId)

    groupId = int(groupId)

    message = "Hello! Welcome to the Target Identification Task. "\
              "I am the Automated Target Detection (ATD) agent and I will help you identify images."

    agentImage = ""
    if groupId == 1 or groupId == 4:
        agentImage = "study5_comp.jpg"
    elif groupId == 2 or groupId == 5:
        agentImage = "study5_avatar.jpg"
    elif groupId == 3 or groupId == 6:
        agentImage = "study5_human.jpg"

    context = {'hash':hash,'enc':enc,'nextRound': round, 'message': message, 'allocationStatement': getAllocationStatement(groupId), 'agentImage': agentImage}
    template = 'study5/initalMessage.html'

    return render(request, template, context)


def begin(request, hash, enc, round):

    maxRound = 6
    mTurkId = decode_data(hash, enc)[0]
    groupId = int(getGroupIdFromMTurkId(mTurkId))

    agentGif = ""

    # TODO identify/check true round number

    numImgToManual = 0
    numImgToAuto = 0
    request.session['startTimeRound' + round] = str(datetime.now())

    if 1 <= int(round) <= maxRound:
        # get the allocation number from the request
        if request.method == 'POST':

            numImgToAuto = 0
            numImgToManual = 0
            if 1 <= int(round) < maxRound:
                numImgToAuto =  request.POST.get('allocationToAutomation')
                numImgToManual = 20 - int(numImgToAuto)

                # Select next agent gif to view
                if groupId == 1 or groupId == 4:
                    agentGif = "Computer-"
                elif groupId == 2 or groupId == 5:
                    agentGif = "Avatar-"
                elif groupId == 3 or groupId == 6:
                    agentGif = "Human-"

                gifOrder = getGifOrder(mTurkId)
                agentGif += str(gifOrder[int(round)-1]) + ".gif"

            # save info from the results page into the DB
            #TODO get time zone offset datetime.strptime(request.POST.get('recordDate'),'%Y-%m-%d %H:%M:%S')
            durationResults = 0
            durationResultPage = 0
            durationGamePage = 0
            if 2 <= int(round) <= maxRound:

                durationResults = request.POST.get('durationResults')
                durationResultPage = request.POST.get('durationResultPage')
                durationGamePage = request.session['durationRound' + str(int(round)-1)]

            Results.objects.create(mTurkId = mTurkId, groupId = groupId, roundNumber = round,
                durationMessage = request.POST.get('durationMessage'), numImgToManual = numImgToManual, numImgToAuto = numImgToAuto,
                durationAllocation = request.POST.get('durationAllocation'), durationResults = durationResults, durationResultPage = durationResultPage,
                durationGamePage = durationGamePage, recordDate = datetime.now())



            if int(round) == maxRound:
                #return HttpResponse("test!")
                # launch the survey page
                context = {"groupId": groupId}
                template = 'study5/survey.html'
                return render(request, template, context)
        else:
            return HttpResponse("Unfortunately, you will not be able to complete the study since the page was refreshed.")

    else:
        return HttpResponse("Invalid round number!")

    #return HttpResponse("gifNumber=%s, agentGif=%s, groupId=%s"%(gifNumber, agentGif, groupId))
    context = {'hash':hash,'enc':enc,'round':round, 'numImgToManual': numImgToManual, 'numImgToAuto' : numImgToAuto,
               'numImgNotProcessed': getAutomationCorrectness(int(numImgToAuto), int(groupId))[1], 'agentGif': agentGif}
    template = 'study5/game.html'
    return render(request, template,context)


@csrf_exempt
def recordAnswers(request, hash, enc, round):

    mTurkId = decode_data(hash,enc)[0]
    groupId = getGroupIdFromMTurkId(mTurkId)

    groupId = int(groupId)

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
            pageDuration = json_data['pageDuration'] # in seconds
            trajectory = json_data['trajectory']

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


        avgTimeAuto = getAvgAutomationTime(numImgAllocatedAuto)
        totalTimeAuto = numImgAllocatedAuto * avgTimeAuto

        #accScore, timeScore, totalScore, avgScore = scoreCalculation(pageDuration,
        #    float(numImgCorrectManual + numImgCorrectAuto)/float(numImgAllocatedManual + numImgAllocatedAuto),groupId)


        rawScore, noiseScore, totalScore = scoreCalculation(numImgAllocatedAuto, int(groupId))
        #return HttpResponse("rawScore=%s, noiseScore=%s, totalScore=%s, groupId = %s"%(rawScore, noiseScore, totalScore, groupId))



        #messageObj = MessagePool.objects.get(groupId = groupId)
        message = "I was unable to identify X images."

        if numImgIncorrectAuto == 1:
            message = message.replace("images", "image ")

        message = message.replace("X", str(int(numImgIncorrectAuto)))

        if numImgAllocatedAuto == 0:
            message = "I did not classify any images."


        agentImage = ""
        if groupId == 1 or groupId == 4:
            agentImage = "study5_comp.jpg"
        elif groupId == 2 or groupId == 5:
            agentImage = "study5_avatar.jpg"
        elif groupId == 3 or groupId == 6:
            agentImage = "study5_human.jpg"



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
                    'totalScore': totalScore,
                    'prevRound':round, 'message': message, 'allocationStatement': getAllocationStatement(int(groupId)), 'agentImage': agentImage}

        #return HttpResponse("accScore=%s, timeScore=%s, totalScore=%s, avgScore = %s, groupId = %s, allocationStatement = %s"%(accScore, timeScore, totalScore, avgScore, groupId, allocationStatement))
        Score.objects.create(mTurkId = mTurkId, groupId = groupId, groupName = getGroupName(groupId), roundNumber = round,
            numImgAllocatedManual = numImgAllocatedManual, numImgAllocatedAuto = numImgAllocatedAuto,
            numImgCorrectManual = numImgCorrectManual, numImgCorrectAuto = numImgCorrectAuto,
            numImgIncorrectManual = numImgIncorrectManual, numImgIncorrectAuto = numImgIncorrectAuto,
            totalTime = pageDuration, totalTimeManual = finishTimeManual, totalTimeAuto = totalTimeAuto,
            avgTimeManual = avgTimeManual, avgTimeAuto = avgTimeAuto, rawScore = rawScore,
            noiseScore = noiseScore, roundScore = totalScore, trajectory = trajectory, recordDate = datetime.now())


        template = 'study5/resultsAndMessages.html'
        return render(request, template, context)
    else:
        return HttpResponse("Something went wrong!")


@csrf_exempt
def checkImageCorrectness(request):

    if request.method == 'POST':
        answer = request.POST['answer']
        imageId = request.POST['imageId']

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

        answer = {"question1": question1, "question2": question2, "question3": question3,
                "question4": question4, "question5":question5, "question6":question6, "question7":question7}


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

        answer = {"question1": question1}

        result = ''
        if question1 == 'option1':
            result = 'ok'

        ConsentPageResults.objects.create(selectedAnswer = json.dumps(answer),width = width, height = height,
            durationPage = request.POST['durationPage'], recordDate = datetime.now())
        return HttpResponse(result)
    else:
        return HttpResponse("Request is not a post!")

def scoreCalculation(numImgAllocatedAuto, groupId):

    lowIdeal = 5.0
    highIdeal = 15.0
    maxScore = 90.0
    score = 0

    # Low reliablity
    if groupId == 1 or groupId == 2 or groupId == 3:
        score = maxScore*(1 - abs(numImgAllocatedAuto - lowIdeal)/20)

    # High reliability
    elif groupId == 4 or groupId == 5 or groupId == 6:
        score = maxScore*(1 - abs(numImgAllocatedAuto - highIdeal)/20)

    # Add noise
    noiseInt = random.randint(0, 300)
    noise = (noiseInt - 150)/100

    totalScore = score + noise

    return score, noise, totalScore


def getAutomationCorrectness(numImgAllocatedAuto, groupId):
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


def getAllocationStatement(groupId):

    # Same alloc statement in every group
    allocationStatement = "Please let me know how many images I should classify in Round"

    return allocationStatement

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


def addMessagesToDb(request):
    # TODO: write a script, improve it, check unique!

    groupId = 0

    # Messages not needed
    # machinelike = "X images unable to be identified."
    # humanlike = "I am sorry that X images were unable to be identified."
    empty = ""

    # Group 1 - 3
    #Low rel
    groupId += 1
    MessagePool.objects.create(groupId = groupId, groupName = "lowReliability-comp",
        groupReliability = "low", message = empty)
    groupId += 1
    MessagePool.objects.create(groupId = groupId, groupName = "lowReliability-avatar",
        groupReliability = "low", message = empty)
    groupId += 1
    MessagePool.objects.create(groupId = groupId, groupName = "lowReliability-human",
        groupReliability = "low", message = empty)

    # Group 4 - 6
    #High rel
    groupId += 1
    MessagePool.objects.create(groupId = groupId, groupName = "highReliability-comp",
        groupReliability = "high", message = empty)
    groupId += 1
    MessagePool.objects.create(groupId = groupId, groupName = "highReliability-avatar",
        groupReliability = "high", message = empty)
    groupId += 1
    MessagePool.objects.create(groupId = groupId, groupName = "highReliability-human",
        groupReliability = "high", message = empty)


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

def generateGifOrder():
    order = [1, 2, 3, 4, 5]
    random.shuffle(order)
    orderString = ""
    for i in order:
        orderString += str(i)
    return orderString

def getGifOrder(mTurkId):
    userObj = Users.objects.get(mTurkId = mTurkId)
    number = userObj.gifOrder
    return number

@csrf_exempt
def assignGroupNumber():
	# TODO: improve this method!
    numberOfGroups = 6
    numberOfUsers = Users.objects.all().count()
    return (numberOfUsers % numberOfGroups) +1

@csrf_exempt
def assignGroupNumber2():

	# TODO: improve this method!!!

    count_actual = Users.objects.values('groupId').order_by('groupId').annotate(the_count=Count('groupId'))

    count_prev = [
            {'the_count': 0, 'groupId': '1'},
            {'the_count': 0, 'groupId': '2'},
            {'the_count': 0, 'groupId': '3'},
            {'the_count': 0, 'groupId': '4'},
            {'the_count': 0, 'groupId': '5'},
            {'the_count': 0, 'groupId': '6'}
    ]


    count_qualtrics = [
            {'the_count': 0, 'groupId': '1'},
            {'the_count': 0, 'groupId': '2'},
            {'the_count': 0, 'groupId': '3'},
            {'the_count': 0, 'groupId': '4'},
            {'the_count': 0, 'groupId': '5'},
            {'the_count': 0, 'groupId': '6'}
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

def page_not_found(request, template_name='study4/404.html'):
    t = loader.get_template("study4/404.html")
    return HttpResponseServerError(render_to_string('study4/404.html', context_instance=RequestContext(request)))

def server_error(request, template_name='study4/500.html'):
    t = loader.get_template("study4/500.html")
    return HttpResponseServerError(render_to_string('study4/500.html', context_instance=RequestContext(request)))

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
    ###Score.objects.all().delete()
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
            {'the_count': 0, 'groupId': '1'},
            {'the_count': 0, 'groupId': '2'},
            {'the_count': 0, 'groupId': '3'},
            {'the_count': 0, 'groupId': '4'},
            {'the_count': 0, 'groupId': '5'},
            {'the_count': 0, 'groupId': '6'}
    ]


    count_qualtrics = [
            {'the_count': 0, 'groupId': '1'},
            {'the_count': 0, 'groupId': '2'},
            {'the_count': 0, 'groupId': '3'},
            {'the_count': 0, 'groupId': '4'},
            {'the_count': 0, 'groupId': '5'},
            {'the_count': 0, 'groupId': '6'}
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

