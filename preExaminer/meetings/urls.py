from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.landingpage,name="landingpage"),
    path('verify/',views.verify,name="verifycard"),
    path('verify/detect/',views.button,name="rolldetect"),
    path('verify/detect/rollnumber',views.rolldetect,name="script"),
    path('viewattendees/',views.attendeelist,name="list"),
    path('attendee_csv/',views.attendee_csv,name='attendee_csv')
]