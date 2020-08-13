var startTimePage, width, height;

function surveyValidateQuestion(e, t) {
    var n = t.data.consent;
    $.ajax({
        url: "/checkConsent/",
        type: "POST",
        data: {
            question1: n,
            width: width,
            height: height,
            durationPage: (new Date - startTimePage) / 1e3
        },
        success: function(e) {
            window.location = "ok" == e ? "/register/" : "/consent_not_given/"
        },
        error: function(e, t, n) {}
    })
}

function displayConsentQuestions() {
    window.survey = new Survey.Model({
        questions: [{
            type: "radiogroup",
            hasOther: !1,
            isRequired: !0,
            name: "consent",
            colCount: 1,
            title: " ",
            choices: [{
                value: "option1",
                text: "I have read the above information, I certify that I am 18 years old or older, and give consent to participate in the study."
            }, {
                value: "option2",
                text: "I choose not to participate in this study."
            }]
        }]
    }), survey.showQuestionNumbers = "off", survey.onComplete.add(function(e) {});
    var e = new showdown.Converter;
    survey.onTextMarkdown.add(function(t, n) {
        var o = e.makeHtml(n.text);
        o = (o = o.substring(3)).substring(0, o.length - 4), n.html = o
    }), $("#surveyElement").Survey({
        model: survey,
        onServerValidateQuestions: surveyValidateQuestion
    }), $(".sv_q_title").css({
        "font-size": "23px"
    }), $(".sv_q_title").html(""), $(".sv_q_radiogroup").css({
        "font-weight": "lighter"
    }), $(".sv_complete_btn").prop("value", "Continue")
}

$(document).ready(function() {
    startTimePage = new Date, displayConsentQuestions(), width = screen.width, height = screen.height
}), history.pushState(null, null, location.href), window.onpopstate = function() {
    history.go(1)
};