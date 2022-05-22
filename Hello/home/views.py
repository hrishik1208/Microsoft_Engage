from io import SEEK_END
from operator import imod
from pickle import TRUE
from re import S
import re
from reprlib import aRepr
from xmlrpc.client import TRANSPORT_ERROR
from cv2 import idct
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
import datetime
import os
from home.models import contact
from home.models import Mains
from home.models import Teacher_reg
from home.models import Student_reg
from home.models import Course
from home.models import Live
from home.models import Course_str
from home.models import Non_approved
from home.models import Approved
from home.models import Student_attendace_report
from home.models import recognize
from home.models import Join
from django.contrib import messages
from django.contrib.auth.models import User,auth
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
import cv2
import cvzone
import numpy as np
import face_recognition
import time
from math import radians, cos, sin, asin, sqrt
from django.http.response import StreamingHttpResponse
import glob
import numpy as np

def index(request): 
    curr=request.user
    d=dict() 
    if Teacher_reg.objects.filter(username=curr.username).exists(): 
        d["name"]=curr.first_name 
        return redirect('/teacher_page') 

    if Student_reg.objects.filter(username=curr.username).exists(): 
        d["name"]=curr.first_name 
        return redirect('/student_page')

    if(request.method=="POST"):
        username=request.POST.get('username')
        password=request.POST.get('password')
        if User.objects.filter(username=username).exists() == False:
            messages.error(request,"Account does not exists")
            return redirect('/')
        c=User.objects.get(username=username)
        D=c.password
        print(D)
        print(password)
        if(D != password):
            return render(request,'err.html')
        if Teacher_reg.objects.filter(username=username).exists():
            d["name"]=c.first_name
            if c is not None:
                auth.login(request,c)
            return redirect('/teacher_page')
        else:
            d["name"]=c.first_name
            if c is not None:
                auth.login(request,c)
            return redirect('/student_page')
        
    return render(request,'Register_login.html')


# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
#  Teacher Part Below  ||
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------



def teach(request):
    d=dict()
    if(len(request.user.username)==0):
        return redirect('/')

    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    if(request.method=="POST"):
        if len(request.user.username) !=0:
            abcd=request.POST.get("hari")
            print(abcd)
            ob=Live.objects.filter(username=request.user.username,course_name=abcd)
            ob.delete()
        else:
            name=request.POST.get('name')
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')
            if User.objects.filter(username=username).exists():
                messages.error(request,"Account with the username already exists")
                return redirect('/')
            else:
                con=Teacher_reg(name=name,email=email,username=username,password=password)
                con.save()
                user=User(username=username,email=email,password=password,first_name=name,last_name=name)
                user.save() 
                if user is not None: 
                    messages.success(request,"Registered Succsessfully") 
                    auth.login(request,user) 

    active=Live.objects.filter(username=request.user.username)
    comments = Course_str.objects.filter(username=request.user.username)
    print("hola",comments)
    past=[] 
    for i in comments: 
        if i.username==request.user.username:
            past.append(i)
    sign=1
    a=round(time.time() * 1000)
    if len(active)==0:
        sign=0
    elif active[0].time_future <= a:
        active.delete()
        sign=0
    else:
        sign=1
    f=request.user.first_name 
    d["name"]=f 
    d["sign"]=sign
    d["active"]=[]
    past.reverse()
    d["past"]=past
    if sign==1:
        d['active']=active[0]
    # print(active[0].course_name)
    return render(request,'teach_page.html',d) 

def course(request): 
    if(len(request.user.username)==0):
        return redirect('/')
    
    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')
    
    d=dict()
    if(request.method=="POST"):
        l= Live.objects.filter(username=request.user.username)
        c_name=request.POST.get('coursename')
        Time=request.POST.get('time')
        Time=int(Time)
        a=round(time.time() * 1000)
        location=request.POST.get('flexRadioDefault')
        print(location)
        
        if len(l)>0:
            A=l[0]
            if A.time_future <= a:
                A.delete()
                l=[]

        if len(l) > 0:
                messages.error(request,"Already one class is going on you account. Please Finish accepting attendance to publish a new attendance ")

        elif Course.objects.filter(username=request.user.username,course_name=c_name).exists() == False:
            messages.error(request,"No such course name found with your account ")

        else :
            latitude=0
            longitude=0
            bool=0
            radius=0
            if location != "onboard":
                bool=1
                location=location.split('+')
                latitude=float(location[0])
                longitude=float(location[1])
                radius=request.POST.get('radius')
            a=round(time.time() * 1000)
            print(a)
            b=a
            a=a+((Time*60)*1000)
            hi=datetime.date.today()
            m1=Live(username=request.user.username,course_name=c_name,time_future=a,attended_list="",date=hi,time_present=b,latitude=latitude,longitude=longitude,bool=bool,radius=radius)
            m1.save()
            gi=0
            m2=Course_str(username=request.user.username,course_name=c_name,date=hi,time_present=b,attended_list="")
            m2.save()
            messages.success(request,"Attendance Published ")

    fg=datetime.date.today()
    print(fg)
    c=request.user
    d["name"]=c.first_name
    l= Course.objects.filter(username=request.user.username)
    print(len(l))
    d["list"]=l
    L=[1,2,3]
    d["H"]=L
    d["y"]=range(0,len(l)) 
    return render(request,'courses.html',d)



def create(request): 
    if(len(request.user.username)==0):
        return redirect('/')
    
    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')
    
    d=dict()
    if(request.method=="POST"):
        c_name=request.POST.get('coursename')
        code=request.POST.get('code')
        if Course.objects.filter(course_name=c_name,username=request.user.username).exists():
            c=request.user
            d["name"]=c.first_name
            c=c.username
            messages.error(request,"The same course is already registered with your account")
        else:
            c=request.user
            d["name"]=c.first_name
            c=c.username
            us=Course(username=c,course_name=c_name,join_code=code)
            us.save()
            messages.success(request,"The course is registered successfully")
        return render(request,'teach_create.html',d)
    
    c=request.user
    d["name"]=c.first_name
    return render(request,'teach_create.html',d)

def insights(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')
    d=dict()
    d["name"]=request.user.first_name
    return render(request,'insights.html',d)

def Request(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    if request.method=="POST":
        s=request.POST.get('hari')
        if s == "Accept_all" :
            li=Non_approved.objects.filter(t_username=request.user.username)
            count=0
            for i in range(0,len(li)):
                count+=1
                ob=li[i]
                ob1=Approved(t_username=request.user.username,t_name=ob.t_name,s_username=ob.s_username,s_email=ob.s_email,s_id=ob.s_id,course_name=ob.course_name,img=ob.img,join_code=ob.join_code)
                ob1.save()
                ob.delete()
            print("count is",count)
        else:
            s=s.split(',')
            li=Teacher_reg.objects.filter(username=request.user.username)
            con=Approved(t_username=request.user.username,t_name=li[0].name,s_username=s[0],s_email=s[3],s_id=s[2],course_name=s[1],img=str(s[0])+"0.jpg",join_code=s[4])
            con.save()
            con1=Non_approved.objects.filter(t_username=request.user.username,s_username=s[0],course_name=s[1])
            con1.delete()
            print(s)

    listt=Non_approved.objects.filter(t_username=request.user.username)
    sign=1
    if len(listt) ==0:
        sign=0

    print(len(listt))
    d=dict()
    d["name"]=request.user.first_name
    d["sign"]=sign
    d["listt"]=listt
    return render(request,'request.html',d)


def run(username):
    cap = cv2.VideoCapture(0)
    i = 0
    h=True
    while(i<5 and cap.isOpened()):
        ret, frame = cap.read()
        
        if h == True:
            cv2.imwrite('media/'+str(username)+'.jpg', frame)
            h=False
        i += 1
    
    cap.release()
    cv2.destroyAllWindows()


# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
#  Student Part Below  ||
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
def Calculate_globe_distance(a,b,c,d,radius):
    print(a,b)
    print(c,d)
    lon1 = radians(c)
    lon2 = radians(d)
    lat1 = radians(a)
    lat2 = radians(b)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    r = 6371
    r=r*c
    r=r*1000
    print("Your distance difference between in metres is ",abs(r))
    if r < abs(radius) :
        return True

    return False

If_posted=False
Response_charge=False
def stu(request): 
    
    d=dict()
    if(request.method=="POST"):
        if len(request.user.username) !=0:  
            hi=request.POST.get("krish")   
            print(hi)
            hi=hi.split(',')
            objectt=Student_attendace_report.objects.filter(t_username=hi[0],s_username=request.user.username,course_name=hi[1],bool=0,time_present=int(hi[2]))
            objectt1=Student_attendace_report.objects.filter(t_username=hi[0],s_username=request.user.username,course_name=hi[1],bool=1,time_present=int(hi[2]))
            if len(objectt1) !=0:
                messages.success(request,"Attendance is already Marked")
            else:
                bool = int(hi[3])
                if bool == 1:
                    print("THIS is hgone inside")
                    location=hi[7]
                    location=location.split('+')
                    if Calculate_globe_distance(float(hi[4]),float(location[0]),float(hi[5]),float(location[1]),float(hi[6])) == False:
                        messages.error(request,"Your Current Location is out of the range which instructor had set In. So please Go to Class to mark it.")
                        return redirect('/')

                global If_posted
                If_posted=True
                global Response_charge
                count=0
                val1=recognize(username=request.user.username,If_posted=1,Response_charge=0)
                val1.save()
                val=recognize.objects.filter(username=request.user.username)
                while val[0].Response_charge == 0:
                    val=recognize.objects.filter(username=request.user.username)
                    count+=1

                val1=recognize(username=val[0].username,If_posted=0,Response_charge=0)
                val1.save()

                img1=cv2.imread('media/'+request.user.username+'_imageno_0.jpg')
                # img1=cv2.imread('media/H.jpg')
                rgb_img1=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
                img1_encoding=face_recognition.face_encodings(rgb_img1)[0]
                img2=cv2.imread('media/'+request.user.username+'trial.jpg')
                rgb_img2=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
                if( len(face_recognition.face_encodings(rgb_img2)) ==0):
                    messages.error(request,"Please Try Again")
                    return redirect('/student_page')
                img2_encoding=face_recognition.face_encodings(rgb_img2)[0]
                result = face_recognition.compare_faces([img1_encoding],img2_encoding)

                if result[0] == True:
                    
                    objectf=Student_attendace_report(t_username=objectt[0].t_username,s_username=request.user.username,course_name=objectt[0].course_name,date=objectt[0].date,bool=1,time_present=objectt[0].time_present)
                    objectf.save()
                    target=Course_str.objects.filter(username= objectt[0].t_username,course_name=objectt[0].course_name,time_present=int(hi[2]))
                    myPythonList =(target[0].attended_list)
                    
                    if(myPythonList==""):
                        myPythonList=str(request.user.email)

                    elif request.user.email not in myPythonList:
                        myPythonList+="!!!!"+str(request.user.email)
                    
                    tarhj=Course_str(username=target[0].username,course_name=target[0].course_name,date=target[0].date,time_present=target[0].time_present,attended_list=myPythonList)
                    tarhj.save()
                    target[0].delete()
                    objectt[0].delete()
                    messages.success(request,"Attendance Marked Successfully")
                    return redirect('/student_page')
                else:
                    messages.error(request,"Face Not matched. Please Mark Again")
                    return redirect('/student_page')
                
        else:
            name=request.POST.get('name')
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')
            val=recognize(username=username,If_posted=0,Response_charge=0)
            val.save()
            val1=Join(username=username,bool=0)
            val1.save()
            if User.objects.filter(username=username).exists():
                messages.error(request,"Account with the username already exists")
                return redirect('/')
            else:
                con=Student_reg(name=name,email=email,username=username,password=password)
                con.save()
                user=User(username=username,email=email,password=password,first_name=name,last_name=name)
                user.save()
                if user is not None:
                    auth.login(request,user)
                    messages.success(request,"Registered Successfully")



    a=round(time.time() * 1000)
    g=Live.objects.exclude(time_future__lt=a)

    # print("lenght ",len(g))
    g1=Approved.objects.filter(s_username=request.user.username)
    final1=[]
    final2=[]
    # print("leng",len(g))
    # print("leng",len(g1))
    for i in g1:
        # print(i.course_name,"hi")
        for j in g:
            # print(j.course_name)
            if (str(j.username)==str(i.t_username)) and (str(j.course_name) == str(i.course_name)):
                # print("REal",j.username)
                if j not in final1:
                    final1.append(j)
                if i not in final2:
                    final2.append(i)


    if(len(request.user.username)==0):
        return redirect('/')
    if Student_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')
    f=request.user.first_name 
    list=Approved.objects.filter(s_username=request.user.username)
    
    print("lenght ",len(final1))
    sign=1
    for i in final1:
        ob1=Student_attendace_report.objects.filter(t_username=i.username,s_username=request.user.username,course_name=i.course_name,date=i.date,bool=1,time_present=i.time_present)
        ob2=Student_attendace_report.objects.filter(t_username=i.username,s_username=request.user.username,course_name=i.course_name,date=i.date,bool=0,time_present=i.time_present)
        if len(ob1) !=0 :
            continue
        elif len(ob2) !=0:
            continue
        else:
            ob1=Student_attendace_report(t_username=i.username,s_username=request.user.username,course_name=i.course_name,date=i.date,bool=0,time_present=i.time_present)
            ob1.save()
        

    if len(final1) ==0:
        sign=0
        d["final"]=[]
    else:
        d["final1"]=final1[0]
        
    d["name"]=f
    d["list"]=list
    
    # print("lenght ",len(final1))
    d["sign"]=sign
    return render(request,'stu_page.html',d)

processing_imageno=0
processing_imagenofake=0


def join(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Student_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    video = cv2.VideoCapture(0)
    # if os.path.exists('media/H1.jpg'):
    #     print("Yes file is there")
    global processing_imageno
    processing_imageno=0
    global processing_imagenofake
    processing_imagenofake=0
    d=dict()
    if request.method=="POST":
        c_name=request.POST.get('coursename')
        code=request.POST.get('code')
        id=request.POST.get('id')
        g=Course.objects.filter(course_name=c_name,join_code=code)
        g1=Non_approved.objects.filter(course_name=c_name,join_code=code,s_username=request.user.username)
        g2=Approved.objects.filter(course_name=c_name,join_code=code,s_username=request.user.username)
        if len(g)==0:
            messages.error(request,"No Instructor found with the given course and join code. Please try again! ")
            return redirect('/')
        elif len(g1) !=0:
            messages.error(request,"Request to Instructor has already been sent by your account previously. ")
            return redirect('/')
        elif len(g2) !=0:
            messages.error(request,"You are already Registered ")
            return redirect('/')
        else:
            print(g)
            count=0
            val1=Join(username=request.user.username,If_posted=1,Response_charge=0)
            val1.save()
            val=Join.objects.filter(username=request.user.username)
            while val[0].Response_charge == 0:
                val=Join.objects.filter(username=request.user.username)
                count+=1

            val1=Join(username=val[0].username,If_posted=0,Response_charge=0)
            val1.save()

            li=Teacher_reg.objects.filter(username=g[0].username)
            li2=Student_reg.objects.filter(username=request.user.username)
            # run(str(request.user.username)+str(li[0].username))
            # print("This ihiowhuowhon",str(request.user.username)+str(li[0].username)+".jpg")
            st = request.user.username+'_imageno_'
            img2=cv2.imread('media/'+request.user.username+'_imageno_'+str(0)+'.jpg')
            rgb_img2=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
            if( len(face_recognition.face_encodings(rgb_img2)) ==0):
                messages.error(request,"Please Try Again")
                return redirect('/')

            else:

                con=Non_approved(t_username=li[0].username,t_name=li[0].name,s_username=request.user.username,s_email=li2[0].email,s_id=id,course_name=c_name,img=st+str(0)+'.jpg',join_code=code)
                con.save()
                messages.success(request,"Request sent to respective Instructor Successfully ")
            return redirect('/')

    d["name"]=request.user.first_name
    messages.success(request,"Your image and Id no. will be processed to Instructor")
    return render(request,'join.html',d)

def profile(request):
    if(len(request.user.username)==0):
        return redirect('/')
        
    if Student_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')
    d=dict()
    d["name"]=request.user.first_name
    return render(request,'profile.html',d)


def cam(request):
    if(request.method == 'POST'):
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


        # saving image to     model part

        # con=Mains(name="kah",img='Frame0.jpg')
        # con.save()
        # print(request.user.username)
        return HttpResponse()

    return render(request,'cam.html')
    

def logout(request):
    user=request.user
    auth.logout(request)
    return redirect('/')

  

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('media/output.avi', fourcc, 20.0, (640, 480))
detector = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
hand_cascade=cv2.CascadeClassifier(r'aGest.xml')
detectorf = FaceDetector()
def gen(request):
    video = cv2.VideoCapture(0)
    accept=True
    count=0
    while True:
        success, image = video.read()
        if success== False:
            continue
        frame_flip = cv2.flip(image,1)
        img, bboxs = detectorf.findFaces(frame_flip)
        gray=cv2.cvtColor(frame_flip,cv2.COLOR_BGR2GRAY)
        all_faces = detector.detectMultiScale(gray,1.5,5)
        
        if len(bboxs)==1:
            center = bboxs[0]["center"]
            for face in all_faces:
                x,y,w,h = all_faces[0]
                rgb_img1=cv2.cvtColor(frame_flip,cv2.COLOR_BGR2RGB)
                val=Join.objects.filter(username=request.user.username)
                if val[0].If_posted == 1 and len(face_recognition.face_encodings(rgb_img1)) >0 :
                    cv2.imwrite('media/'+str(request.user.username)+'_imageno_'+str(0)+'.jpg', frame_flip)
                    val1=Join(username=val[0].username,If_posted=0,Response_charge=1)
                    val1.save()

        elif len(bboxs)>1:
            pass

        else:
            cv2.putText(frame_flip,'No face detected',(10, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),2,cv2.LINE_AA)
        
            # cv2.putText(frame_flip,'No face detected',(10, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),2,cv2.LINE_AA)

        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



def video_feed(request):
    return StreamingHttpResponse(gen(request),content_type='multipart/x-mixed-replace; boundary=frame')

detectorh=HandDetector(detectionCon=0.8, maxHands=1)

def gen1(request):
    video = cv2.VideoCapture(0)
    accept=True
    count=0
    while True:
        success, image = video.read()
        if success== False:
            continue
        frame_flip = cv2.flip(image,1)
        hands=detectorh.findHands(frame_flip,draw=False)
        img, bboxs = detectorf.findFaces(frame_flip)

        # gray=cv2.cvtColor(frame_flip,cv2.COLOR_BGR2GRAY)
        # all_faces = detector.detectMultiScale(gray,1.5,5)

        # if len(all_faces)>0:
        #     for face in all_faces:
        #         x,y,w,h = face
        #         rgb_img1=cv2.cvtColor(frame_flip,cv2.COLOR_BGR2RGB)
        #         global If_posted
        #         global Response_charge
        #         if If_posted == True and len(face_recognition.face_encodings(rgb_img1)) >0 :
        #             cv2.imwrite('media/'+str(request.user.username)+'trial.jpg', frame_flip)
        #             If_posted=False
        #             Response_charge=True

        #         cv2.rectangle(frame_flip, (x, y), (x+w,y+h), (0, 0, 255), 2)
        #     cv2.putText(frame_flip,'Face detected',(330, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 128,0),2,cv2.LINE_AA)
        # else:
        #     cv2.putText(frame_flip,'No Face detected',(10, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),2,cv2.LINE_AA)
        
        if hands:
            x,y,w,h = hands[0]['bbox']
            cvzone.putTextRect(frame_flip,'',(x,y))
            cv2.rectangle(frame_flip, (x, y), (x+w,y+h), (255, 0, 255), 2)

        else:
            cv2.putText(frame_flip,'No Hands detected',(10, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),2,cv2.LINE_AA)
        
        gray=cv2.cvtColor(frame_flip,cv2.COLOR_BGR2GRAY)
        all_faces = detector.detectMultiScale(gray,1.5,5)
        if len(bboxs)==1:
            center = bboxs[0]["center"]
            for face in all_faces:
                x,y,w,h = all_faces[0]
                val=recognize.objects.filter(username=request.user.username)
                rgb_img1=cv2.cvtColor(frame_flip,cv2.COLOR_BGR2RGB)
                global If_posted
                global Response_charge
                if val[0].If_posted == 1 and len(face_recognition.face_encodings(rgb_img1)) >0 and len(hands)>0 :
                    cv2.imwrite('media/'+str(request.user.username)+'trial.jpg', frame_flip)
                    val1=recognize(username=val[0].username,If_posted=0,Response_charge=1)
                    val1.save()
        elif len(bboxs)>1:
            pass
        else:
            cv2.putText(frame_flip,'No Face detected',(350, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),2,cv2.LINE_AA)

        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed_1(request):
    return StreamingHttpResponse(gen1(request),content_type='multipart/x-mixed-replace; boundary=frame')


