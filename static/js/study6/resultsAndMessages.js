var startTimePage, endTimeResults, endTimeMessage, allocationToManual = 10;

function enableBtn(a) {
    // after round 5, we do not show the waiting for partner text.
    // thats why: if the text exists

    if (document.getElementById("waiting-txt")) {
        function enableHelper() {
            document.getElementById("waiting-txt").innerHTML = "Your partner has signaled ready."
            document.getElementById("waiting-txt").style.color = "green";
            document.getElementById("begin-btn").disabled = false;
        }

        if (a === "HUMAN") {
            window.setTimeout(enableHelper, Math.floor((Math.random() * 2500) + 2500));
        } else {
            document.getElementById("waiting-txt").innerHTML = ""
            document.getElementById("begin-btn").disabled = false;
        }
    }
}

function nextTrial() {
    var e = $("#allocationToAutomation").val(),
        t = " image ",
        a = " image ";
    return e > 1 && (a = " images "), allocationToManual > 1 && (t = " images "), $("#dialog-confirm-text").html('<span class="ui-icon ui-icon-alert" style="float:left; margin:12px 12px 20px 0;"></span>Partner: ' + e + a + "<br>Operator (You): " + allocationToManual + t), $("#dialog-confirm").dialog({
        height: "auto",
        width: 400,
        modal: !0,
        buttons: {
            "Yes, I am sure": function() {
                return $("#durationResults").val((endTimeResults - startTimePage) / 1e3), $("#durationMessage").val((endTimeMessage - endTimeResults) / 1e3), $("#durationAllocation").val((new Date - endTimeMessage) / 1e3), $("#durationResultPage").val((new Date - startTimePage) / 1e3), $("#recordDate").val(new Date), $("#ResultsInputForm").submit(), !0
            },
            "No, I want to change": function() {
                return $(this).dialog("close"), !1
            }
        }
    }), !1
}

function lastRound() {
    return $("#durationResults").val((endTimeResults - startTimePage) / 1e3), $("#durationMessage").val((endTimeMessage - endTimeResults) / 1e3), $("#durationAllocation").val((new Date - endTimeMessage) / 1e3), $("#durationResultPage").val((new Date - startTimePage) / 1e3), $("#recordDate").val(new Date), $("#ResultsInputForm").submit(), !0
}

function drawGauge(e, t) {
    Highcharts.setOptions({
        colors: ["#F03E3E", "#f6931f", "#FFDD00", "#bbe529", "#30B32D"]
    }), $("#" + e).highcharts({
        chart: {
            renderTo: "container",
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: !1
        },
        title: {
            text: "Round Score",
            align: "center",
            verticalAlign: "top",
            fontSize: "18px",
            y: 80
        },
        tooltip: {
            formatter: function() {
                return this.series.name + ":" + this.point.x * this.point.y + "--" + (this.point.x + 1) * this.point.y
            }
        },
        pane: {
            center: ["50%", "75%"],
            size: "50%",
            startAngle: 0,
            endAngle: 100,
            background: {
                borderWidth: 0,
                backgroundColor: "none",
                innerRadius: "20%",
                outerRadius: "100%",
                shape: "arc"
            }
        },
        yAxis: [{
            lineWidth: 0,
            min: 0,
            max: 100,
            minorTickLength: 0,
            tickLength: 0,
            tickWidth: 0,
            labels: {
                enabled: !1
            },
            title: {
                text: '<div class="gaugeFooter"><strong>' + t + "/100</strong></div>",
                useHTML: !0,
                y: 80
            },
            pane: 0
        }],
        plotOptions: {
            pie: {
                dataLabels: {
                    enabled: !0,
                    distance: -50,
                    style: {
                        fontWeight: "bold",
                        color: "white",
                        fontSize: "16px",
                        textShadow: "0px 1px 3px black"
                    }
                },
                startAngle: -90,
                endAngle: 90,
                center: ["50%", "75%"]
            },
            series: {
                colorByPoint: !0
            },
            gauge: {
                dataLabels: {
                    enabled: !1
                },
                dial: {
                    radius: "100%"
                }
            }
        },
        credits: {
            enabled: !1
        },
        series: [{
            type: "pie",
            name: "Score",
            innerSize: "50%",
            data: [
                ["Poor", 20],
                ["Fair", 20],
                ["Good", 20],
                ["Great", 20],
                ["Excellent", 20]
            ]
        }, {
            type: "gauge",
            data: [getDataFeedbackValue(t)],
            dial: {
                rearLength: 1
            }
        }]
    })
}

function getDataFeedbackValue(e) {
    return parseFloat(e) / 100 * 164 - 82
}

$(document).ready(function() {
    startTimePage = new Date,
    drawGauge("gauge-graph", parseInt(totalScore)),
    document.getElementById("resultsButtonDiv").style.display = "block";
    var e = 5,
        t = setInterval(function() {
            e <= 0 ? (clearInterval(t), $("#results-button").prop("disabled", !1), $("#results-next-timer").remove(), $("#results-button").append('<i class="icon-arrow-right"></i>')) : (e--, $("#results-next-timer").text("Wait! " + e))
        }, 1e3),
        a = $("#custom-handle");
    $("#slider").slider({
        create: function() {
            a.text($(this).slider("value"))
        },
        slide: function(e, t) {
            a.text(t.value), $("#allocationToAutomation").val(t.value), allocationToManual = 20 - parseInt(t.value)
        },
        classes: {
            "ui-slider": "highlight"
        },
        range: "min",
        value: 10,
        min: 0,
        max: 20,
        animate: "fast"
    }), $("#allocationToAutomation").val($("#slider").slider("value"))
}), history.pushState(null, null, location.href), window.onpopstate = function() {
    history.go(1)
}, $("#message-button").on("click", function() {
    endTimeMessage = new Date,
    document.getElementById("allocationDiv").style.display = "block",
    $("#message-button").prop("disabled", !0),
    $(enableBtn(partner));
}), $("#results-button").on("click", function() {
    endTimeResults = new Date,
    document.getElementById("messageDiv").style.display = "block",
    $("#results-button").prop("disabled", !0);
    new TypeIt("#message", {
        speed: 60,
        cursor: !0,
        lifeLike: !0,
        cursorChar: "|"
    }).type(message).options({
        afterComplete: function(e) {
            e.destroy(), document.getElementById("messageButtonDiv").style.display = "block"
        }
    });
    var e = 5,
        t = setInterval(function() {
            e <= 0 ? (clearInterval(t), $("#message-button").prop("disabled", !1), $("#message-next-timer").remove(), $("#message-button").append('<i class="icon-arrow-down"></i>')) : (e--, $("#message-next-timer").text("Wait! " + e))
        }, 1e3)
});
