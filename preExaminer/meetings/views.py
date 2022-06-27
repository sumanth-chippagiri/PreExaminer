from django.shortcuts import render
from django.http import HttpResponse
from . import models
from PIL import Image
from pytesseract import pytesseract
import cv2
import time
from .models import rollnumber
import datetime
import csv

def attendee_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=attendees.csv'

    writer=csv.writer(response)
    attendees=rollnumber.objects.all()
    writer.writerow(['Roll Number','Name','Branch'])
    for attendee in attendees:
        writer.writerow([attendee.rollno,attendee.name,attendee.branch])


    return response
    


def landingpage(request):
    return render(request,'meetings/landingpage.html')

def verify(request):
    return render(request,'meetings/verifycard.html')

def button(request):
    return render(request,'meetings/rolldetect.html')

def attendeelist(request):
    attendee_list=rollnumber.objects.distinct()
    return render(request,'meetings/attendees.html',{'attendee_list':attendee_list})
def rolldetect(request):
    camera_port=0
    camera = cv2.VideoCapture(camera_port,cv2.CAP_DSHOW)
    while True:
        _,Image =camera.read()
        cv2.imshow('Card at center of window',Image)
        if cv2.waitKey(1)&0xFF==ord('q'):
            camera.release()
            cv2.destroyAllWindows()
            break

    first=160119000000
    last=160119999999
    rollnumbers_range=[]
    for each_roll in range(first,last+1):
        rollno_string=str(each_roll)
        rollnumbers_range.append(rollno_string)
        #rollnumbers_range.append('160119736052')
        #if cv2.waitKey(1)&0xFF==ord('q'):
        #cv2.imwrite('card.jpg', Image)
    rollno=""
    path_to_tesseract="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    #Imagepath='card.jpg'
    pytesseract.tesseract_cmd=path_to_tesseract
    text=pytesseract.image_to_string(Image)

    print(text)
    for s in text:
        if s.isdigit():
            rollno+=s
    data=""
    name=""
    for rno in rollnumbers_range:
        if rno in rollno:
            #print(f"Detected roll number is: {rno}")
            data=rno
            break
    name=""
    start=text.find("Name")
    start=start+4
    end=text.find("Father")
    name_string=text[start:end]
    for i in name_string:
        if i.isalpha():
            name+=i
        elif i==" ":
            name+=" "
    
    course=""
    start=text.find("Course")
    start=start+6
    end=text.find("SEM")
    course=text[start:end]
    course+=" SEM"

    end=end+3
    branch=""
    for i in range(end,end+4):
        if text[i].isalpha():
            branch+=text[i]

    if(data):
        rno_instance=rollnumber.objects.create(rollno=data,name=name,branch=branch)

    print(data)
    context = {
        'data':data,
        'name':name,
        #'course':course,
        'branch':branch
        #'sub':sub
    }
    
    return render(request,'meetings/rolldetect.html',context)
