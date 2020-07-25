var startTimePage, numberOfAttempt = 0;

function surveyValidateQuestion(e, t) {
    var o = t.data.innocentVehicle,
        a = t.data.enemyVehicle,
        r = t.data.scoreCalculation,
        i = t.data.markerLocation,
        n = t.data.markerColor,
        s = "" + t.data.comments,
        c = t.data.checkSound;
    $.ajax({
        url: "/checkInstructionQuestions/",
        type: "POST",
        data: {
            question1: o,
            question2: a,
            question3: r,
            question4: i,
            question5: n,
            question6: s,
            question7: c,
            hash: hash,
            enc: enc,
            numberOfAttempt: ++numberOfAttempt,
            durationPage: (new Date - startTimePage) / 1e3
        },
        success: function(e) {
            "6" == e ? window.location = "/instructionRisk/" + hash + "/" + enc + "/" + round + "/" : "5" == e ? alert("1 of your answer is not correct. Please read the instructions above and then answer the questions again.") : alert(6 - parseInt(e) + " of your answers are not correct. Please read the instructions above and then answer the questions again.")
        },
        error: function(e, t, o) {}
    })
}

function displayInstCheckQuestions() {
    var e = {
        questions: [{
            type: "radiogroup",
            hasOther: !1,
            isRequired: !0,
            name: "innocentVehicle",
            colCount: 2,
            title: "Which of the images below is a non-dangerous vehicle?",
            choices: [{
                value: "car1",
                text: "![A car1](" + static_url + "images/car20.jpg)"
            }, {
                value: "car2",
                text: "![A car2](" + static_url + "images/car11.jpg)"
            }, {
                value: "car3",
                text: "![A car3](" + static_url + "images/car16.jpg)"
            }, {
                value: "car4",
                text: "![A car4](" + static_url + "images/car1.jpg)"
            }]
        }, {
            type: "radiogroup",
            hasOther: !1,
            isRequired: !0,
            name: "enemyVehicle",
            colCount: 2,
            title: "Which of the images below is a dangerous vehicle?",
            choices: [{
                value: "car1",
                text: "![A car1](" + static_url + "images/car8.jpg)"
            }, {
                value: "car2",
                text: "![A car2](" + static_url + "images/car9.jpg)"
            }, {
                value: "car3",
                text: "![A car3](" + static_url + "images/car17.jpg)"
            }, {
                value: "car4",
                text: "![A car4](" + static_url + "images/car4.jpg)"
            }]
        }, {
            type: "radiogroup",
            hasOther: !1,
            isRequired: !0,
            name: "scoreCalculation",
            colCount: 1,
            title: "Which of the following correctly describes the scoring calculation in this game?",
            choices: [{
                value: "option1",
                text: "Only accuracy is important to get the highest score. <br> In other words, no matter how long it takes, if one identifies images correctly, he/she will get the highest score."
            }, {
                value: "option2",
                text: "Only time is important to get the highest score. <br> In other words, if one identifies images as quickly as possible regardless of his/her accuracy, he/she will get the highest score."
            }, {
                value: "option3",
                text: "Both time and accuracy are important to get the highest score. <br> In other words, if one identifies images correctly as quickly as possible, he/she will get the highest score."
            }, {
                value: "option4",
                text: "Neither time nor accuracy is important, <br> because everybody gets the same score regardless of their accuracy or how long it takes. "
            }]
        }, {
            name: "markerLocation",
            type: "radiogroup",
            isRequired: !0,
            title: "Where is the operator's drone (the drone you will control), located at the beginning of each round?",
            choices: [{
                value: "option1",
                text: "At the lower left corner of the Operator’s Panel"
            }, {
                value: "option2",
                text: "At the top left corner of the Operator’s Panel"
            }, {
                value: "option3",
                text: "At the lower right corner of the Operator’s Panel"
            }, {
                value: "option4",
                text: "At the top right corner of the Operator’s panel"
            }]
        }, {
            name: "markerColor",
            type: "radiogroup",
            isRequired: !0,
            title: "Which markers do you need to select on the map to examine images?",
            choices: [{
                value: "option1",
                text: "The orange markers <img src=\"https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_orange.png\"> on the map"
            }, {
                value: "option2",
                text: "The blue markers <img src=\"https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_blue.png\"> on the map"
            }, {
                value: "option3",
                text: "Both the blue <img src=\"https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_blue.png\"> and orange <img src=\"https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_orange.png\"> markers on the map"
            }, {
                value: "option4",
                text: "None of them"
            }]
        }, {
            type: "comment",
            name: "comments",
            isRequired: !0,
            title: "In your own words, please briefly summarize the instructions in this page."
        }, {
            name: "checkSound",
            type: "radiogroup",
            isRequired: !0,
            title: "Please turn on your speaker, click the play button below and choose the number that you hear: <br> <br><audio controls controlsList='nodownload'><source src='" + static_url + "sound/number-sound.mp3' type='audio/mp3'>Your browser does not support the audio element.</audio>",
            choices: [{
                value: "option1",
                text: "4"
            }, {
                value: "option2",
                text: "7"
            }, {
                value: "option3",
                text: "9"
            }, {
                value: "option4",
                text: "20"
            }]
        }]
    };
    window.survey = new Survey.Model(e), survey.onComplete.add(function(e) {});
    var t = new showdown.Converter;
    survey.onTextMarkdown.add(function(e, o) {
        var a = t.makeHtml(o.text);
        a = (a = a.substring(3)).substring(0, a.length - 4), o.html = a
    }), $("#surveyElement").Survey({
        model: survey,
        onServerValidateQuestions: surveyValidateQuestion
    }), $(".sv_q_title").css({
        "font-size": "23px"
    }), $(".sv_q_radiogroup").css({
        "font-weight": "lighter"
    }), $(".sv_complete_btn").prop("value", "Continue")
}


$(document).ready(function() {
    startTimePage = new Date,
    displayInstCheckQuestions()
}), history.pushState(null, null, location.href), window.onpopstate = function() {
    history.go(1)
};