var startTimePage,endTimeResults,endTimeMessage;function nextTrial(){var e=$("#allocationToAutomation").val(),a=$("#allocationToManual").val(),t="image was ",n="image was ";return e>1&&(n="images were "),a>1&&(t="images were "),$("#dialog-confirm-text").html('<span class="ui-icon ui-icon-alert" style="float:left; margin:12px 12px 20px 0;"></span>'+e+" "+n+"assigned to the automation, and "+a+" "+t+"assigned to yourself for the next round. Are you sure?"),$("#dialog-confirm").dialog({height:"auto",width:400,modal:!0,buttons:{"Yes, I am sure":function(){return $("#durationResults").val((endTimeResults-startTimePage)/1e3),$("#durationMessage").val((endTimeMessage-endTimeResults)/1e3),$("#durationAllocation").val((new Date-endTimeMessage)/1e3),$("#durationResultPage").val((new Date-startTimePage)/1e3),$("#recordDate").val(new Date),$("#ResultsInputForm").submit(),!0},"No, I want to change":function(){return $(this).dialog("close"),!1}}}),!1}$(document).ready(function(){startTimePage=new Date;var e=$("#custom-handle");$("#slider").slider({create:function(){e.text($(this).slider("value"))},slide:function(t,n){e.text(n.value),$("#slider2").slider("value",20-parseInt(n.value)),a.text(20-parseInt(n.value)),$("#allocationToAutomation").val(n.value),$("#allocationToManual").val(20-parseInt(n.value)),$("#aImageAllocation").text(n.value),$("#mImageAllocation").text(20-parseInt(n.value))},classes:{"ui-slider":"highlight"},range:"min",value:10,min:0,max:20,animate:"fast"});var a=$("#custom-handle2");$("#slider2").slider({create:function(){a.text($(this).slider("value"))},slide:function(t,n){a.text(n.value),$("#slider").slider("value",20-parseInt(n.value)),e.text(20-parseInt(n.value)),$("#allocationToManual").val(n.value),$("#allocationToAutomation").val(20-parseInt(n.value)),$("#mImageAllocation").text(n.value),$("#aImageAllocation").text(20-parseInt(n.value))},classes:{"ui-slider":"highlight"},range:"min",value:10,min:0,max:20,animate:"fast"}),$("#allocationToAutomation").val($("#slider").slider("value")),$("#allocationToManual").val($("#slider2").slider("value")),6==parseInt(round)&&$("#allocation-question").html("<h3 class='text-center'>If you were to play another round in which there would be 20 images to examine, how many images would you want to assign to the Automation in that round? </h3>");var t=1,n=setInterval(function(){t<=0?(clearInterval(n),$("#results-button").prop("disabled",!1),$("#results-next-timer").remove(),$("#results-button").append('<i class="icon-arrow-right"></i>')):(t--,$("#results-next-timer").text("Wait! "+t))},1e3)}),videojs("avatar_video").on("ended",function(){console.log("Video Ended!");var e=1,a=setInterval(function(){e<=0?(clearInterval(a),$("#message-button").prop("disabled",!1),$("#message-next-timer").remove(),$("#message-button").append('<i class="icon-arrow-down"></i>')):(e--,$("#message-next-timer").text("Wait! "+e))},1e3)}),$("#results-button").on("click",function(){endTimeResults=new Date,document.getElementById("messageDiv").style.display="block",videojs("avatar_video").play(),$("#results-button").prop("disabled",!0)}),$("#message-button").on("click",function(){endTimeMessage=new Date,document.getElementById("allocationDiv").style.display="block",$("#message-button").prop("disabled",!0)});