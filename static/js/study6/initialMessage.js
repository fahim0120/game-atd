var startTimePage, endTimeMessage=0, allocationToManual = 10;


// This function is called from the html page. Button onclick= return nextTrial()
function nextTrial() {
    var e = $("#allocationToAutomation").val(),
        a = " image ",
        t = " image ";
    return e > 1 && (t = " images "), allocationToManual > 1 && (a = " images "),
    $("#dialog-confirm-text").html('<span class="ui-icon ui-icon-alert" style="float:left; margin:12px 12px 20px 0;"></span>Partner: ' + e + t + "<br>Operator (You): " + allocationToManual + a),
    $("#dialog-confirm").dialog({
        height: "auto",
        width: 400,
        modal: !0,
        buttons: {
            "Yes, I am sure": function() {
                return $("#durationMessage").val((endTimeMessage - startTimePage) / 1e3), $("#durationAllocation").val((new Date - endTimeMessage) / 1e3), $("#recordDate").val(new Date), $("#ResultsInputForm").submit(), !0
            },
            "No, I want to change": function() {
                return $(this).dialog("close"), !1
            }
        }
    }), !1
}


function enableBtn(a) {
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


function previewVideo() {

    var video = document.getElementById('preview');

    navigator.mediaDevices.getUserMedia({
        audio: false,
        video: true
    }).then(function(stream) {
        setSrcObject(stream, video);

        video.play();
        video.muted = true;

        recorder = new RecordRTCPromisesHandler(stream, {
            mimeType: 'video/webm',
            bitsPerSecond: 128000
        });

        recorder.stream = stream;
        document.getElementById("cameraNextButtonDiv").style.display = "block";

        $.ajax({
            url: "/recordCameraPermission/",
            type: "POST",
            data: {
                hash: hash,
                enc: enc,
                yes_no: 'yes'
            },
            success: function(e) {
                //"3" == e ? window.location = "/initialMessage/" + hash + "/" + enc + "/" + round + "/" : "2" == e ? alert("1 of your answer is not correct. Please read the instructions above and then answer the questions again.") : alert(3 - parseInt(e) + " of your answers are not correct. Please read the instructions above and then answer the questions again.")
            },
            error: function(e, t, o) {}
        })


    }).catch(function(error) {
        console.error("Cannot access media devices: ", error);
        //document.getElementById("cameraPermissionDeniedMessage").style.display = "block";
        document.getElementById("cameraNextButtonDiv").style.display = "block";

        $.ajax({
            url: "/recordCameraPermission/",
            type: "POST",
            data: {
                hash: hash,
                enc: enc,
                yes_no: 'no'
            },
            success: function(e) {
                //"3" == e ? window.location = "/initialMessage/" + hash + "/" + enc + "/" + round + "/" : "2" == e ? alert("1 of your answer is not correct. Please read the instructions above and then answer the questions again.") : alert(3 - parseInt(e) + " of your answers are not correct. Please read the instructions above and then answer the questions again.")
            },
            error: function(e, t, o) {}
        })

    });

}


function displayCameraDiv() {
    if (endTimeMessage !== 0) {
        endTimeMessage = new Date;
    }
    document.getElementById("cameraPanel").style.display = "block",
    $("#next-button").prop("disabled", !0),
    $("#overlay").fadeOut(900),
    $("#message").css("z-index", "0"),
    previewVideo();
}


function displayAllocationDiv() {
    if (endTimeMessage !== 0) {
        endTimeMessage = new Date;
    }
    document.getElementById("allocationDiv").style.display = "block",
    $("#next-button").prop("disabled", !0),
    $("#overlay").fadeOut(900),
    $("#message").css("z-index", "0"),
    $(enableBtn(partner))
}


$(document).ready(function() {
    startTimePage = new Date, $("#message").css("z-index", "99999"), $("#overlay").fadeIn(900);

    new TypeIt("#introMessage", {
        speed: 60,
        cursor: !0,
        lifeLike: !0,
        cursorChar: "|"
    }).type(messageTxt).options({
        afterComplete: function(e) {
            e.destroy(), document.getElementById("nextButtonDiv").style.display = "block"
        }
    });
    var e = $("#custom-handle");
    $("#slider").slider({
        create: function() {
            e.text($(this).slider("value"))
        },
        slide: function(a, t) {
            e.text(t.value), $("#allocationToAutomation").val(t.value), allocationToManual = 20 - parseInt(t.value)
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
}), $("#next-button").on("click", function() {
    if (partner === "HUMAN") {
        displayCameraDiv();
    } else {
        displayAllocationDiv();
    }
}), $("#camera-next-button").on("click", function() { // NEW
    displayAllocationDiv();
}), history.pushState(null, null, location.href), window.onpopstate = function() {
    history.go(1)
};



