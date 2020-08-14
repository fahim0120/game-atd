"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import settings
#import views                 # Study-1
#import views_map2 as views   # Study-2
#import views_study3 as views  # Study-3
#import views_study4 as views  # Study-4
#import views_study5 as views  # Study-5
import views_study6 as views  # Study-6


urlpatterns = [

    ##############################Study-1#########################################

    #url(r'^$', views.viewInfoSheetPage),
    #url(r'^checkConsent/$',views.checkConsent),
    #url(r'^consent_not_given/$',views.viewConsentNotGivenMessage),
    #url(r'^register2/$',views.register_user),
    #url(r'^begin2/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.begin),
    #url(r'^next2/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.recordAnswers),
    #url(r'^add_image2/$',views.addImagesToDb),
    #url(r'^add_message2/$',views.addMessagesToDb),
    #url(r'^checkImage/$',views.checkImageCorrectness),
    #url(r'^checkInstructionQuestions/$',views.checkInstructionCorrectness),
    #url(r'^instruction2/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInstructionPage),
    #url(r'^initialMessage2/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInitialMessage),


    ##############################Study-2#########################################

    #url(r'^$', views.viewInfoSheetPage),
    #url(r'^checkConsent/$',views.checkConsent),
    #url(r'^consent_not_given/$',views.viewConsentNotGivenMessage),
    #url(r'^register2/$',views.register_user),
    #url(r'^begin2/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.begin),
    #url(r'^next2/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.recordAnswers),
    #url(r'^checkImage/$',views.checkImageCorrectness),
    #url(r'^checkInstructionQuestions/$',views.checkInstructionCorrectness),
    #url(r'^instruction2/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInstructionPage),
    #url(r'^initialMessage2/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInitialMessage),
    ####
    #url(r'^add_image2/$',views.addImagesToDb),
    #url(r'^add_message2/$',views.addMessagesToDb),


    ##############################Study-3#########################################

    #url(r'^$', views.viewInfoSheetPage),
    #url(r'^checkConsent/$',views.checkConsent),
    #url(r'^consent_not_given/$',views.viewConsentNotGivenMessage),
    ####
    #'''
    #url(r'^register/$',views.register_user),
    #url(r'^begin/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.begin),
    #url(r'^next/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.recordAnswers),
    #url(r'^checkImage/$',views.checkImageCorrectness),
    #url(r'^checkInstructionQuestions/$',views.checkInstructionCorrectness),
    #url(r'^instruction/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInstructionPage),
    #url(r'^initialMessage/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInitialMessage),
    #'''
    ####
    #url(r'^add_image2/$',views.addImagesToDb),
    #url(r'^add_message2/$',views.addMessagesToDb),


    ##############################Study-4#########################################


    #url(r'^$', views.viewInfoSheetPage),
    #url(r'^checkConsent/$',views.checkConsent),
    #url(r'^consent_not_given/$',views.viewConsentNotGivenMessage),

    #url(r'^register/$',views.register_user),
    #url(r'^begin/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.begin),
    #url(r'^next/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.recordAnswers),
    #url(r'^checkImage/$',views.checkImageCorrectness),
    #url(r'^checkInstructionQuestions/$',views.checkInstructionCorrectness),
    #url(r'^instruction/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInstructionPage),
    #url(r'^initialMessage/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInitialMessage),

    ####
    #url(r'^add_images/$',views.addImagesToDb),
    #url(r'^add_messages/$',views.addMessagesToDb),



    ##############################Study-5#########################################


    #url(r'^$', views.viewInfoSheetPage),
    #url(r'^checkConsent/$',views.checkConsent),
    #url(r'^consent_not_given/$',views.viewConsentNotGivenMessage),

    #url(r'^register/$',views.register_user),
    #url(r'^begin/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.begin),
    #url(r'^next/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.recordAnswers),
    #url(r'^checkImage/$',views.checkImageCorrectness),
    #url(r'^checkInstructionQuestions/$',views.checkInstructionCorrectness),
    #url(r'^instruction/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInstructionPage),
    #url(r'^initialMessage/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInitialMessage),

    ####
    #url(r'^add_images/$',views.addImagesToDb),
    #url(r'^add_messages/$',views.addMessagesToDb),



    ##############################Study-6#########################################


    url(r'^$', views.viewInfoSheetPage),
    url(r'^checkConsent/$', views.checkConsent),
    url(r'^consent_not_given/$', views.viewConsentNotGivenMessage),

    url(r'^register/$', views.register_user),
    url(r'^begin/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.begin),
    url(r'^next/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.recordAnswers),
    url(r'^checkImage/$',views.checkImageCorrectness),
    url(r'^checkInstructionQuestions/$', views.checkInstructionCorrectness),
    url(r'^instruction/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInstructionPage),
    url(r'^checkInstructionRiskQuestions/$', views.checkInstructionRiskCorrectness),
    url(r'^instructionRisk/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInstructionRiskPage),
    url(r'^initialMessage/(?P<hash>.+)/(?P<enc>.+)/(?P<round>\d+)/$', views.viewInitialMessage),
    url(r'^recordCameraPermission/$', views.recordCameraPermission),

    ####
    #url(r'^add_images/$',views.addImagesToDb),
    #url(r'^add_messages/$',views.addMessagesToDb),
    url('admin/', admin.site.urls),


	##############################Test#########################################
	url(r'^test1/', views.test),
	url(r'^test2/', views.test2),
    url(r'^test3/', views.test3),
    url(r'^test4/', views.test4),

]


