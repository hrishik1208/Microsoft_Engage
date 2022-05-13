from pickle import TRUE
from xmlrpc.client import TRANSPORT_ERROR
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import contact
from home.models import Mains
from home.models import Teacher_reg
from home.models import Student_reg
from django.contrib import messages
from django.contrib.auth.models import User,auth
import cv2
import face_recognition

def index(request): 
    if(request.method=="POST"):
        d=dict()
        username=request.POST.get('username')
        password=request.POST.get('password')
        if User.objects.filter(username=username).exists() == False:
            return render(request,'err.html')
        c=User.objects.get(username=username)
        D=c.password
        print(D)
        print(password)
        if(D != password):
            return render(request,'err.html')
        if Teacher_reg.objects.filter(username=username).exists():
            d["name"]=str(c.first_name)
            if c is not None:
                auth.login(request,c)
            return render(request,'teach_page.html',d)
        else:
            d["name"]=str(c.first_name)
            if c is not None:
                auth.login(request,c)
            return render(request,'stu_page.html',d)
        
    return render(request,'Register_login.html')

def teach(request):
    if(request.method=="POST"):
        d=dict()
        name=request.POST.get('name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request,'err.html')
        else:
            con=Teacher_reg(name=name,email=email,username=username,password=password)
            con.save()
            user=User(username=username,email=email,password=password,first_name=name,last_name=name)
            user.save()
            if user is not None:
                auth.login(request,user)
        d["name"]=name
        return render(request,'teach_page.html',d)
    
    else:
        return render(request,'err.html')

def stu(request): 
    if(request.method=="POST"):
        d=dict()
        name=request.POST.get('name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request,'err.html')
        else:
            con=Student_reg(name=name,email=email,username=username,password=password)
            con.save()
            user=User(username=username,email=email,password=password,first_name=name,last_name=name)
            user.save()
            if user is not None:
                auth.login(request,user)
        d["name"]=name
        return render(request,'stu_page.html',d)
    else:
        return render(request,'err.html')


def run():
    cap = cv2.VideoCapture(0)
    i = 0
    h=True
    while(i<5 and cap.isOpened()):
        ret, frame = cap.read()
        
        if h == True:
            cv2.imwrite('media/Frame'+str(i)+'.jpg', frame)
            h=False
        
        i += 1
    
    cap.release()
    cv2.destroyAllWindows()


def cam(request):
    if(request.method == 'POST'):
        #saving images into media directpory part

        run()
        # iu=Mains.objects.get(name="kshh")
        # ipg=cv2.imread('static/1.jpg',1)
        # print(iu.img)
        # ipg=cv2.imread(str(iu.img),1)
        # cv2.imshow('vacd',ipg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        
        # Detecting the faces.

        # image = face_recognition.load_image_file("media/H1.jpg")
        # face_locations = face_recognition.face_locations(image)
        # print(face_locations)
        
        # recognition part
       
        # img1=cv2.imread('media/H1.jpg')
        # img2=cv2.imread('media/Frame0.jpg')
        # rgb_img1=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
        # img1_encoding=face_recognition.face_encodings(rgb_img1)[0]

        # rgb_img2=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
        # img2_encoding=face_recognition.face_encodings(rgb_img2)[0]

        # result = face_recognition.compare_faces([img1_encoding],img2_encoding)


        # saving image to model part

        # con=Mains(name="kah",img='Frame0.jpg')
        # con.save()
        # print(request.user.username)
        return HttpResponse()

    return render(request,'cam.html')