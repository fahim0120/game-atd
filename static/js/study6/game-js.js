var startTimeImageExamination, startTimePage, finishTimeManual, mapObject, data = {},
    amountToChange = 10,
    zoomInOutSpeed = 100,
    countCompletedImages = 0,
    countZoomIn = 0,
    countZoomOut = 0,
    results = [],
    automationDone = !1,
    numberOfCorrectManual = 0,
    numberOfIncorrectManual = 0,
    trajectory = [],
    markerCount = 0,
    manualImageArray = [];
    manualImageCounter = 0;
var prevFlightPosition = new google.maps.LatLng(41.759, -72.786),
    prevFlightPositionATD = new google.maps.LatLng(41.75937, -72.600423),
    automationLocationArray = [],
    ATDMarkers = [],
    ATDLocationIndexes = [],
    manualMarkers = [],
    automationArray = [],
    workingOnIdentification = !1,
    droneCircle = null,
    alertInactivity = !1,
    planeSymbol = {
        path: "M22.1,15.1c0,0-1.4-1.3-3-3l0-1.9c0-0.2-0.2-0.4-0.4-0.4l-0.5,0c-0.2,0-0.4,0.2-0.4,0.4l0,0.7c-0.5-0.5-1.1-1.1-1.6-1.6l0-1.5c0-0.2-0.2-0.4-0.4-0.4l-0.4,0c-0.2,0-0.4,0.2-0.4,0.4l0,0.3c-1-0.9-1.8-1.7-2-1.9c-0.3-0.2-0.5-0.3-0.6-0.4l-0.3-3.8c0-0.2-0.3-0.9-1.1-0.9c-0.8,0-1.1,0.8-1.1,0.9L9.7,6.1C9.5,6.2,9.4,6.3,9.2,6.4c-0.3,0.2-1,0.9-2,1.9l0-0.3c0-0.2-0.2-0.4-0.4-0.4l-0.4,0C6.2,7.5,6,7.7,6,7.9l0,1.5c-0.5,0.5-1.1,1-1.6,1.6l0-0.7c0-0.2-0.2-0.4-0.4-0.4l-0.5,0c-0.2,0-0.4,0.2-0.4,0.4l0,1.9c-1.7,1.6-3,3-3,3c0,0.1,0,1.2,0,1.2s0.2,0.4,0.5,0.4s4.6-4.4,7.8-4.7c0.7,0,1.1-0.1,1.4,0l0.3,5.8l-2.5,2.2c0,0-0.2,1.1,0,1.1c0.2,0.1,0.6,0,0.7-0.2c0.1-0.2,0.6-0.2,1.4-0.4c0.2,0,0.4-0.1,0.5-0.2c0.1,0.2,0.2,0.4,0.7,0.4c0.5,0,0.6-0.2,0.7-0.4c0.1,0.1,0.3,0.1,0.5,0.2c0.8,0.2,1.3,0.2,1.4,0.4c0.1,0.2,0.6,0.3,0.7,0.2c0.2-0.1,0-1.1,0-1.1l-2.5-2.2l0.3-5.7c0.3-0.3,0.7-0.1,1.6-0.1c3.3,0.3,7.6,4.7,7.8,4.7c0.3,0,0.5-0.4,0.5-0.4S22,15.3,22.1,15.1z",
        fillColor: "#DDDDDD",
        fillOpacity: 1.5,
        scale: 1.2,
        anchor: new google.maps.Point(11, 11),
        strokeWeight: 0
    };

function shuffle(e) {
    for (var t, n, o = e.length; o; t = parseInt(Math.random() * o), n = e[--o], e[o] = e[t], e[t] = n);
    return e
}

function sortNumber(e, t) {
    return e - t
}

function populateImages(e, t, n) {
    for (var o = [], a = 1; a <= e + t; a++) o.push(a);
    o = shuffle(o), e > 0 && $("#placeHolderNoManualImg").remove();
    for (var i = 0; i < o.slice(0, e).length; i++) manualImageArray.push(o[i]);
    t > 0 && $("#placeHolderNoAutoImg").remove()
}

function moveFlight(e, t, n) {
    var o, a, i = e,
        r = t;
    o = new google.maps.Polyline({
        path: [i, r],
        strokeColor: "#0f0",
        strokeWeight: 0,
        icons: [{
            icon: planeSymbol,
            offset: "0%"
        }],
        map: mapObject,
        geodesic: !0
    }), a = new google.maps.Polyline({
        path: [i, i],
        strokeColor: "#2eacd0",
        strokeWeight: 2,
        map: mapObject,
        geodesic: !0
    });
    var l = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame,
        s = !1;
    window.cancelAnimationFrame(s), s = l(function() {
        tick(i, r, o, a, s, 0, n)
    })
}

function tick(e, t, n, o, a, i, r) {
    i += 1.5;
    var l = google.maps.geometry.spherical.interpolate(e, t, i / 100);
    if (o.setPath([e, l]), n.icons[0].offset = Math.min(i, 100) + "%", n.setPath(n.getPath()), i >= 100) {
        if ((window.cancelAnimationFrame || window.mozCancelAnimationFrame)(a), i = 0, "manual" == r) {
            displayVehicleIdentificationDiv();
            var s = manualImageArray[manualImageCounter];
            $("#imageDiv").html('<img id="carImage' + s + '" src=' + static_url + "images/car" + s + '.jpg class="mx-auto d-block" width="100" height="100" >'), startTimeImageExamination = new Date, manualImageCounter++
        }
    } else {
        var c = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
        a = c(function() {
            tick(e, t, n, o, a, i, r)
        })
    }
}

function loadMap() {
    var e = {
        draggable: !1,
        panControl: !1,
        streetViewControl: !1,
        scrollwheel: !1,
        scaleControl: !1,
        disableDefaultUI: !0,
        disableDoubleClickZoom: !0,
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.SATELLITE,
        center: new google.maps.LatLng(41.818764, -72.693277),
        styles: [{
            featureType: "administrative",
            stylers: [{
                visibility: "off"
            }]
        }, {
            featureType: "poi",
            stylers: [{
                visibility: "simplified"
            }]
        }, {
            featureType: "road",
            elementType: "labels",
            stylers: [{
                visibility: "simplified"
            }]
        }, {
            featureType: "water",
            stylers: [{
                visibility: "simplified"
            }]
        }, {
            featureType: "transit",
            stylers: [{
                visibility: "simplified"
            }]
        }, {
            featureType: "landscape",
            stylers: [{
                visibility: "simplified"
            }]
        }, {
            featureType: "road.highway",
            stylers: [{
                visibility: "off"
            }]
        }, {
            featureType: "road.local",
            stylers: [{
                visibility: "on"
            }]
        }, {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [{
                visibility: "on"
            }]
        }, {
            featureType: "water",
            stylers: [{
                color: "#84afa3"
            }, {
                lightness: 52
            }]
        }, {
            stylers: [{
                saturation: -17
            }, {
                gamma: .36
            }]
        }, {
            featureType: "transit.line",
            elementType: "geometry",
            stylers: [{
                color: "#3f518c"
            }]
        }]
    };
    (mapObject = new google.maps.Map(document.getElementById("mapCanvas"), e)).addListener("tilesloaded", function(e) {
        $(".dismissButton").click()
    }), setInterval(function() {
        $("*").each(function() {
            100 == $(this).css("zIndex") && $(this).css("zIndex", "-100")
        })
    }, 500), google.maps.event.addListenerOnce(mapObject, "idle", function() {
        drawRectangle(mapObject), ATD()
    })
}

function drawRectangle(e) {
    for (var t, n = e.getBounds(), o = n.getSouthWest(), a = n.getNorthEast(), i = (a.lng() - o.lng()) / 4, r = (a.lat() - o.lat()) / 5, l = 0, s = null, c = 0; c < 4; c++)
        for (var m = 0; m < 5; m++) {
            var u = 0;
            u = c % 2 != 0 ? 5 - m - 1 : m;
            var g = {
                    north: o.lat() + r * (u + 1),
                    south: o.lat() + r * u,
                    east: o.lng() + i * (c + 1),
                    west: o.lng() + i * c
                },
                d = !1,
                p = !1,
                f = "";
            ++l <= numImgToManual ? (s = "#7BEBE5", t = "https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_blue" + l + ".png", p = !0, f = "Location-" + l) : (s = "#ff7904", t = "https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_orange" + l + ".png", d = !0, f = "Assigned to the automation");
            var h = new google.maps.Rectangle({
                strokeColor: "#000000",
                strokeWeight: 2,
                fillColor: s,
                fillOpacity: .1,
                map: e,
                bounds: g
            });
            if (l % 5 == 0) var v = h.getBounds().getCenter().lat() - r / 2 * Math.random(),
                y = h.getBounds().getCenter().lng() - i / 3 * Math.random();
            else v = h.getBounds().getCenter().lat() + r / 6 * Math.random(), y = h.getBounds().getCenter().lng() + i / 3 * Math.random();
            var I = new google.maps.LatLng(v, y),
                w = new google.maps.Marker({
                    position: I,
                    map: e,
                    area: g,
                    title: f,
                    icon: t,
                    zIndex: Math.round(-1e5 * I.lat()) << 5
                });
            d && (automationLocationArray.push(new google.maps.LatLng(w.getPosition().lat(), w.getPosition().lng())), ATDMarkers.push(w), ATDLocationIndexes.push(l));
            new google.maps.InfoWindow({
                disableAutoPan: !0
            });
            p && google.maps.event.addListener(w, "click", function(t, n) {
                return function() {
                    if (workingOnIdentification) {
                        $("#imageDiv").css("border", "4px solid red"), $("#imageDiv").fadeTo(100, .1).fadeTo(200, 1).fadeTo(100, .1).fadeTo(200, 1).fadeTo(100, .1).fadeTo(200, 1);
                        var o = new google.maps.Size(0, 0);
                        5 == n ? o = new google.maps.Size(40, 60) : 6 == n || 15 == n ? o = new google.maps.Size(0, 70) : 16 == n && (o = new google.maps.Size(-40, 80));
                        var a = new google.maps.InfoWindow({
                            disableAutoPan: !0,
                            pixelOffset: o
                        });
                        a.setContent('<p class="warning-skip"><b>Please finish current <br>vehicle identification</b></p>'), a.open(e, t), setTimeout(function() {
                            a.close(), $("#imageDiv").css("border", "4px solid rgb(221, 221, 221")
                        }, 1e3)
                    } else {
                        droneCircle.setMap(null);
                        moveFlight(prevFlightPosition, new google.maps.LatLng(t.getPosition().lat(), t.getPosition().lng()), "manual"), prevFlightPosition = new google.maps.LatLng(t.getPosition().lat(), t.getPosition().lng()), resetVehicleIdentificationDiv(), manualMarkers.push(t), workingOnIdentification = !0, trajectory.push(n)
                    }
                }
            }(w, l))
        }
}

function findMinDistance(e, t) {
    for (var n = Number.MAX_VALUE, o = null, a = 0; a < t.length; a++) {
        var i = google.maps.geometry.spherical.computeDistanceBetween(e, t[a]);
        n >= i && (n = i, o = t[a])
    }
    return o
}

function remove_item(e, t) {
    var n = "";
    for (n in e)
        if (e[n] === t) {
            e.splice(n, 1);
            break
        }
    return e
}

function orderLocationsGreedy(e, t) {
    for (var n = [], o = t.slice(0), a = 0; a < t.length; a++) e = findMinDistance(e, o), n.push(e), o = remove_item(o, e);
    return n
}

function orderLocations(e) {
    return e.reverse()
}

function findMarkerIndex(e, t) {
    new google.maps.LatLng(t.lat(), t.lng());
    for (var n = 0; n < e.length; n++)
        if (t.lat() == e[n].getPosition().lat() && t.lng() == e[n].getPosition().lng()) return n;
    return -1
}

function addIcon(e, t) {
    var n = new google.maps.InfoWindow({
        disableAutoPan: !0,
        pixelOffset: new google.maps.Size(-20, 60)
    });
    n.setContent(e), n.open(mapObject, ATDMarkers[findMarkerIndex(ATDMarkers, t)])
}

function ATD() {
    var e;
    e = orderLocations(automationLocationArray);
    var t = [],
        n = ATDLocationIndexes.slice(0);
    t = (t = shuffle(n)).slice(0, numImgNotProcessed);
    var o = 0,
        a = 0,
        i = 0,
        r = null;
    $.each(e, function(n, l) {
        setTimeout(function() {
            if (moveFlight(prevFlightPositionATD, e[n], "ATD"), prevFlightPositionATD = e[n], n > 0) {
                var s = null; - 1 == jQuery.inArray(ATDLocationIndexes[n - 1], t) ? (s = '<i class="icon-ok-sign greenInfoBuble"></i>', o++) : (s = '<i class="icon-question-sign blueInfoBuble"></i>', a++), addIcon(s, r), i = Number(o) + Number(a), $("#automationAccScore").html("Accuracy: " + Number(o) + "/" + i), $("#automationAccScore").fadeTo(100, .1).fadeTo(200, 1)
            }
            n == e.length - 1 && setTimeout(function() {
                automationDone = !0;
                var e = null;
                (-1 == jQuery.inArray(ATDLocationIndexes[n], t) ? (e = '<i class="icon-ok-sign greenInfoBuble"></i>', o++) : (e = '<i class="icon-question-sign blueInfoBuble"></i>', a++), addIcon(e, l), i = Number(o) + Number(a), $("#automationAccScore").html("Accuracy: " + Number(o) + "/" + i), $("#automationAccScore").fadeTo(100, .1).fadeTo(200, 1), countCompletedImages == numImgToManual) && sendData((new Date - startTimePage) / 1e3)
            }, autoSpeed), r = l // 3e3
        }, autoSpeed * n) // 3e3
    })
}

function zoomIn() {
    var e = $("#imageDiv").find("img");
    if (e.length > 0) {
        var t = e.first().attr("id"),
            n = ($("#" + t).width(), $("#" + t).height());
        "block" === document.getElementById("alertMaxMinZoomLevel").style.display && (document.getElementById("alertMaxMinZoomLevel").style.display = "none"), n >= 390 ? (document.getElementById("alertMaxMinZoomLevel").style.display = "block", $("#alertMaxMinZoomLevel").html('<p class="text-danger"> Maximum zoom-in level was reached!</p>')) : ($("#" + t).animate({
            height: "+=" + amountToChange + "px",
            width: "+=" + amountToChange + "px"
        }, {
            duration: zoomInOutSpeed
        }), countZoomIn++)
    }
}

function zoomOut() {
    var e = $("#imageDiv").find("img");
    if (e.length > 0) {
        var t = e.first().attr("id"),
            n = $("#" + t).width();
        $("#" + t).height();
        "block" === document.getElementById("alertMaxMinZoomLevel").style.display && (document.getElementById("alertMaxMinZoomLevel").style.display = "none"), n <= 50 ? (document.getElementById("alertMaxMinZoomLevel").style.display = "block", $("#alertMaxMinZoomLevel").html('<p class="text-danger"> Minimum zoom-out level was reached!</p>')) : ($("#" + t).animate({
            height: "-=" + amountToChange + "px",
            width: "-=" + amountToChange + "px"
        }, {
            duration: zoomInOutSpeed
        }), countZoomOut++)
    }
}

function decisionYesNo(e) {
    workingOnIdentification = !1;
    var t = (new Date - startTimeImageExamination) / 1e3,
        n = $("#imageDiv").find("img");
    if (n.length > 0) {
        var o = n.first().attr("id"),
            a = o.substring("carImage".length, o.length);
        $("#imageId" + a).val(a), $("#durationToAnswer" + a).val(t), $("#answer" + a).val(e), $("#countZoomIn" + a).val(countZoomIn), $("#countZoomOut" + a).val(countZoomOut);
        var i = {
            imageId: a,
            countZoomIn: countZoomIn,
            countZoomOut: countZoomOut,
            answer: e,
            durationToAnswer: t,
            responseDate: new Date
        };
        if (results.push(i), countZoomIn = 0, countZoomOut = 0, resetVehicleIdentificationDiv(), $("#imageTile" + a).fadeTo("slow", .44), $("#imageTile" + a).append('<div class="disabledImageTile"></div>'), $.ajax({
                url: "/checkImage/",
                type: "POST",
                data: {
                    answer: e,
                    imageId: a
                },
                success: function(e) {
                    if ($("#correctness" + a).css("display", "block"), "Correct" == e) {
                        $("#correctness" + a).append('<i class="icon-ok-sign text-success"></i>'), numberOfCorrectManual++, new Audio(static_url + "sound/correct.mp3").play();
                        var t = '<i class="icon-ok-sign greenInfoBuble"></i>';
                        (n = new google.maps.InfoWindow({
                            disableAutoPan: !0,
                            pixelOffset: new google.maps.Size(-20, 60)
                        })).setContent(t), n.open(mapObject, manualMarkers[manualImageCounter - 1])
                    } else if ("Incorrect" == e) {
                        $("#correctness" + a).append('<i class="icon-remove-sign text-danger"></i>'), numberOfIncorrectManual++, new Audio(static_url + "sound/bad-beep-incorrect.mp3").play();
                        var n;
                        t = '<i class="icon-remove-sign redInfoBuble"></i>';
                        (n = new google.maps.InfoWindow({
                            disableAutoPan: !0,
                            pixelOffset: new google.maps.Size(-20, 60)
                        })).setContent(t), n.open(mapObject, manualMarkers[manualImageCounter - 1])
                    }
                    var o = Number(numberOfCorrectManual) + Number(numberOfIncorrectManual);
                    $("#manualAccScore").html("Accuracy: " + Number(numberOfCorrectManual) + "/" + o), $("#manualAccScore").fadeIn(100).fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100)
                },
                error: function(e, t, n) {}
            }), ++countCompletedImages == numImgToManual) {
            finishTimeManual = (new Date - startTimePage) / 1e3;
            var r = (new Date - startTimePage) / 1e3;
            automationDone ? sendData(r) : automationDone || $("#imageDiv2").html("<h2></h2>")
        }
    }
}

function displayVehicleIdentificationDiv() {
    document.getElementById("vehicleIdentification").style.display = "block", document.getElementById("vehicleIdentificationPlaceHolder").style.display = "none"
}

function resetVehicleIdentificationDiv() {
    document.getElementById("vehicleIdentificationPlaceHolder").style.display = "block", document.getElementById("vehicleIdentification").style.display = "none"
}

function sendData(e) {
    var t = {
        results: results,
        numImgToAuto: numImgToAuto,
        numImgToManual: numImgToManual,
        finishTimeManual: finishTimeManual,
        pageDuration: e,
        trajectory: trajectory
    };
    $('#ImageInputForm [name="Data"]').val(JSON.stringify(t)), $("#ImageInputForm").submit()
}
$(document).ready(function() {
    if (-1 != document.cookie.indexOf("cookie-for-refresh")) return -1 == document.cookie.indexOf("alertInactivity") && alert("Unfortunately, you will not be able to complete the study since the page was refreshed."), !1;
    document.cookie = "cookie-for-refresh=1";
    screen.width, screen.height;
    startTimePage = new Date, 0 == numImgToManual ? ($("#imageDiv2").html("<h2></h2>"), finishTimeManual = 0) : finishTimeManual = new Date;
    $("#timer").runner({
        autostart: !0,
        countdown: !0,
        startAt: 12e4,
        stopAt: 0
    }).on("runnerFinish", function(e, t) {
        finishTimeManual = (new Date - startTimePage) / 1e3;
        var n = (new Date - startTimePage) / 1e3;
        if (0 == countCompletedImages && numImgToManual > 0) return alert("Unfortunately, you will not be able to complete the study because you did not complete any of the manual images."), document.cookie = "alertInactivity=1", location.reload(), !1;
        alert("Time is up!"), sendData(n)
    }), $(window).resize(function() {
        Math.round(100 * window.devicePixelRatio)
    });
    var e = [61, 107, 173, 109, 187, 189];
    $(document).keydown(function(t) {
        1 == t.ctrlKey && -1 != e.indexOf(t.which) && t.preventDefault()
    }), $(window).bind("mousewheel DOMMouseScroll", function(e) {
        1 == e.ctrlKey && e.preventDefault()
    }), populateImages(numImgToManual, numImgToAuto, round), 0 == numImgToAuto && (automationDone = !0);
    var t = 110,
        n = setInterval(function() {
            t < 1 ? (clearInterval(n), new Audio(static_url + "sound/10-sec-countdown.mp3").play()) : t--
        }, 1e3);
    loadMap(), moveFlight(prevFlightPosition, prevFlightPosition, "initial"), moveFlight(prevFlightPositionATD, prevFlightPositionATD, "initial"), droneCircle = new google.maps.Circle({
        strokeColor: "#FF0000",
        strokeOpacity: .7,
        strokeWeight: 3,
        fillColor: "#FF0000",
        fillOpacity: .15,
        map: mapObject,
        center: prevFlightPosition,
        radius: 520
    });
    var o = 1;
    setInterval(function() {
        var e = droneCircle.getRadius();
        (e > 600 || e < 300) && (o *= -1), droneCircle.setRadius(e + 10 * o)
    }, 50);
    var a = 10,
        i = setInterval(function() {
            a < 1 ? (clearInterval(i), droneCircle.setMap(null)) : a--
        }, 1e3)
});
var angle = 0;

function rotate() {
    var e = $("#imageDiv").find("img").first().attr("id"),
        t = e.substring("carImage".length, e.length);
    angle = (angle + 90) % 360, $("#carImage" + t).css("transform", "rotate(" + angle + "deg)")
}

function createMarker(e, t, n, o) {
    var a = "<b>" + t + "</b><br>" + n,
        i = new google.maps.Marker({
            position: e,
            map: mapObject,
            title: t,
            icon: "https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_red" + ++markerCount + ".png",
            zIndex: Math.round(-1e5 * e.lat()) << 5
        });
    i.myname = t;
    var r = new google.maps.InfoWindow({
        size: new google.maps.Size(150, 50)
    });
    return google.maps.event.addListener(i, "click", function() {
        r.setContent(a), r.open(mapObject, i)
    }), i
}
history.pushState(null, null, location.href), window.onpopstate = function() {
    history.go(1)
}, document.onkeydown = function() {
    switch (event.keyCode) {
        case 116:
            return event.returnValue = !1, event.keyCode = 0, !1;
        case 82:
            if (event.ctrlKey) return event.returnValue = !1, event.keyCode = 0, !1
    }
};

if (partner === "HUMAN") {
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
    }).catch(function(error) {
        console.error("Cannot access media devices: ", error);
    });
}