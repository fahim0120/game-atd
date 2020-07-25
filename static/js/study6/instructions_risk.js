var startTimePage, numberOfAttempt = 0;

function surveyValidateQuestion(e, t) {
    var q1 = t.data.whoIsPartner,
        q2 = t.data.maxCompensation;

    $.ajax({
        url: "/checkInstructionRiskQuestions/",
        type: "POST",
        data: {
            question1: q1,
            question2: q2,
            hash: hash,
            enc: enc,
            numberOfAttempt: ++numberOfAttempt,
            durationPage: (new Date - startTimePage) / 1e3,
            risk: risk,
            partner: partner
        },
        success: function(e) {
            "2" == e ? window.location = "/initialMessage/" + hash + "/" + enc + "/" + round + "/" : "1" == e ? alert("1 of your answer is not correct. Please read the instructions above and then answer the questions again.") : alert("Both of your answers are not correct. Please read the instructions above and then answer the questions again.")
        },
        error: function(e, t, o) {}
    })
}

function displayInstCheckQuestions() {
    var e = {
        questions: [
        {
            type: "radiogroup",
            hasOther: !1,
            isRequired: !0,
            name: "whoIsPartner",
            colCount: 1,
            title: "Who is your partner in this game?",
            choices: [{
                value: "HUMAN",
                text: "Another Mechanical Turk worker."
            }, {
                value: "ATD",
                text: "An automated target detection system."
            }]
        }, {
            type: "radiogroup",
            hasOther: !1,
            isRequired: !0,
            name: "maxCompensation",
            colCount: 2,
            title: "What is the maximum amount of compensation you can earn by completing this study?",
            choices: [{
                value: "option1",
                text: "$3.00"
            }, {
                value: "option2",
                text: "$6.00"
            }, {
                value: "option3",
                text: "$9.00"
            }, {
                value: "option4",
                text: "$12.00"
            }]
        }
        ]
    };

    window.survey = new Survey.Model(e), survey.onComplete.add(function(e) {});
    var t = new showdown.Converter;
    survey.onTextMarkdown.add(function(e, o) {
        var a = t.makeHtml(o.text);
        a = (a = a.substring(3)).substring(0, a.length - 4), o.html = a
    }),
    $("#surveyElement").Survey({
        model: survey,
        onServerValidateQuestions: surveyValidateQuestion
    }),
    $(".sv_q_title").css({
        "font-size": "23px"
    }),
    $(".sv_q_radiogroup").css({
        "font-weight": "lighter"
    }),
    $(".sv_complete_btn").prop("value", "Continue")
}

$(document).ready(function() {
    startTimePage = new Date,
    displayInstCheckQuestions()
}), history.pushState(null, null, location.href), window.onpopstate = function() {
    history.go(1)
};
