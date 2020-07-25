var startTimePage, endTimeResults, endTimeMessage;
$(document).ready(function() {
    startTimePage = new Date, $("#message").css("z-index", "99999"), $("#overlay").fadeIn(900);
    new TypeIt("#introMessage", {
        speed: 80,
        cursor: !0,
        lifeLike: !0,
        cursorChar: "|"
    }).type(message).options({
        afterComplete: function(e) {
            e.destroy(), document.getElementById("nextButtonDiv").style.display = "block"
        }
    })
}), $("#message-button").on("click", function() {
    alert("Hello");
    endTimeMessage = new Date - startTimePage, window.location = "/begin2/" + hash + "/" + enc + "/" + round + "/"
}), history.pushState(null, null, location.href), window.onpopstate = function() {
    history.go(1)
};