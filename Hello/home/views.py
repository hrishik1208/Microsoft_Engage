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
from home.models import mapping

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
from django.core.mail import send_mail


#
#   Login / Register Page code below
#


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
        if(D != password):
            messages.error(request,"Password Not Matched")
            return redirect('/')

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
#  Teacher's Side -> ||
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------

#
# Teacher's Side  |=> Home page 
#

def teach(request):
    d=dict()

    if(request.method=="POST"):
        if len(request.user.username) !=0:
            course_name=request.POST.get("hari")
            ob=Live.objects.filter(username=request.user.username,course_name=course_name)
            ob.delete()
        else:
            name=request.POST.get('name')
            username=request.POST.get('username')
            email=request.POST.get('email')
            comma=','
            if comma in email:
                messages.error(request,"Your email should not contain comma")
                return render('/')
            password=request.POST.get('password')
            if User.objects.filter(username=username).exists():
                messages.error(request,"Account with the username already exists")
                return redirect('/')
            if User.objects.filter(email=email).exists():
                messages.error(request,"Account with the email already exists")
                return redirect('/')
            else:
                con=Teacher_reg(name=name,email=email,username=username,password=password)
                con.save()
                user=User(username=username,email=email,password=password,first_name=name,last_name=name)
                user.save() 
                if user is not None: 
                    messages.success(request,"Registered Succsessfully") 
                    auth.login(request,user) 
                    
    if(len(request.user.username)==0):
        return redirect('/')

    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    active=Live.objects.filter(username=request.user.username)
    comments = Course_str.objects.filter(username=request.user.username)
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

    return render(request,'teach_page.html',d) 

#
# Teacher's Side  |=> My Courses page 
#

def course(request): 
    if(len(request.user.username)==0):
        return redirect('/')
    
    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')
    
    d=dict()
    if(request.method=="POST"):
        l= Live.objects.filter(username=request.user.username)
        c_name=request.POST.get('course_name')
        Time=request.POST.get('time')
        Time=int(Time)
        a=round(time.time() * 1000)
        location=request.POST.get('flexRadioDefault')
        if len(l)>0:
            A=l[0]
            if A.time_future <= a:
                A.delete()
                l=[]

        if len(l) > 0:
                messages.error(request,"Already one class is going on you account. Please Stop accepting attendance to publish a new attendance ")

        elif Course.objects.filter(username=request.user.username,course_name=c_name).exists() == False:
            messages.error(request,"No such course name found with your account ")

        else :
            latitude=0
            longitude=0
            bool=0
            radius=0
            if location != "onboard":
                radius=request.POST.get('radius')
                bool=1
                location=location.split('+')
                latitude=float(location[0])
                longitude=float(location[1])
                radius=request.POST.get('radius')
            a=round(time.time() * 1000)
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
    c=request.user 
    d["name"]=c.first_name 
    l= Course.objects.filter(username=request.user.username) 
    d["list"]=l 
    L=[1,2,3] 
    d["H"]=L 
    d["y"]=range(0,len(l)) 
    d["num"]=len(l) 
    return render(request,'courses.html',d) 

#
# Teacher's Side  |=> Create a course page 
#


def create(request): 
    if(len(request.user.username)==0):
        return redirect('/')
    
    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')
    
    d=dict()
    if(request.method=="POST"):
        c_name=request.POST.get('coursename')
        
        radio=request.POST.get("flexRadioDefault")
        if Course.objects.filter(course_name=c_name,username=request.user.username).exists():
            c=request.user
            d["name"]=c.first_name
            c=c.username
            messages.error(request,"The same course is already registered with your account")
        else:
            c=request.user
            d["name"]=c.first_name
            c=c.username
            len_course=Course.objects.filter()
            len_course=len(len_course)*10 + 111111  
            us=Course(username=c,course_name=c_name,join_code= len_course)
            us.save()
            mapping_object=mapping(join_code=len_course,Course_name=c_name)
            if radio == "noemail":
                email=request.POST.get('email')
                email=email.split(',')
                teacher_info=User.objects.filter(username=request.user.username)
                message="Hello Student, Kindly join the course - " +str(c_name) +" with the join code "+str(len_course)+"\n \n Your Instructor," + "\n " + str(teacher_info[0].first_name) 
                title="Kindly Join the course"
                send_mail(
                    title,
                    message,
                    'attendance.portal.1234@gmail.com',
                    email,
                    fail_silently=False,
                )
                messages.success(request,"The course is registered successfully and mails to students for joining the course has also been sent.")
                return redirect('/course')
            else:
                messages.success(request,"The course is registered successfully")
                return redirect('/course')
            return redirect('/course')
    
    c=request.user
    d["name"]=c.first_name
    return render(request,'teach_create.html',d)

#
# Teacher's Side  |=> Records page of past attendance publishes
#


def insights(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')


    d=dict() 
    if request.method=="POST": 
        present_time=request.POST.get('detail') 
        object=Course_str.objects.filter(username=request.user.username,time_present=int(present_time)) 
        final_attended=[] 
        final_unattended=[] 
        given=object[0].attended_list 
        given=given.split("!!!!") 
        data=Approved.objects.filter(t_username=request.user.username,course_name=object[0].course_name) 
        email_list_unattended=""
        Email_list_unattended=[]
        for i in data: 
            student_email=i.s_email 
            student_id=i.s_id 
            obb=Student_reg.objects.filter(email=student_email) 
            student_name=obb[0].name  
            if student_email in given: 
                dictionary=dict() 
                dictionary["name"]=student_name 
                dictionary["email"]=student_email 
                dictionary["id"]=student_id 
                final_attended.append(dictionary) 
            else: 
                dictionary=dict() 
                dictionary["name"]=student_name 
                dictionary["email"]=student_email 
                dictionary["id"]=student_id 
                final_unattended.append(dictionary) 
                if len(email_list_unattended)==0:
                    email_list_unattended += student_email
                else:
                    email_list_unattended += ','+student_email

                Email_list_unattended.append(student_email)

 
        d["name"]=request.user.first_name 
        d["final_attended"]=final_attended 
        d["final_unattended"]=final_unattended 
        d["course"]=object[0].course_name 
        d["date"]=object[0].date 
        d["No_of_attended"]=len(final_attended) 
        d["No_of_unattended"]=len(final_unattended) 
        d["total"]=len(final_attended)+len(final_unattended) 
        d["list_email"]=email_list_unattended
        d["List_email"]=Email_list_unattended
        return render(request,'detail.html',d) 
        
    data=Course_str.objects.filter(username=request.user.username)
    d["name"]=request.user.first_name
    data1=[]
    for i in data:
        data1.append(i)
    
    data1.reverse()
    d["data"]=data1
    return render(request,'insights.html',d)

#
# Teacher's Side  |=> Pending Requests page 
#


def Request(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    if request.method=="POST":
        s=request.POST.get('hari')
        if_reject= "!!!!"
        if s == "Accept_all" :
            li=Non_approved.objects.filter(t_username=request.user.username)
            count=0
            for i in range(0,len(li)):
                count+=1
                ob=li[i]
                ob1=Approved(t_username=request.user.username,t_name=ob.t_name,s_username=ob.s_username,s_email=ob.s_email,s_id=ob.s_id,course_name=ob.course_name,img=ob.img,join_code=ob.join_code)
                ob1.save()
                ob.delete()
        elif if_reject in s :
            s=s[4:]
            s=s.split(',')
            li=Teacher_reg.objects.filter(username=request.user.username)
            con1=Non_approved.objects.filter(t_username=request.user.username,s_username=s[0],course_name=s[1])
            con1.delete()
            messages.success(request, 'Rejected')
            return redirect('/Request')
        else:
            s=s.split(',')
            li=Teacher_reg.objects.filter(username=request.user.username)
            con=Approved(t_username=request.user.username,t_name=li[0].name,s_username=s[0],s_email=s[3],s_id=s[2],course_name=s[1],img=str(s[0])+"_imageno_0"+str(s[1])+".jpg",join_code=s[4])
            con.save()
            con1=Non_approved.objects.filter(t_username=request.user.username,s_username=s[0],course_name=s[1])
            con1.delete()
        
        messages.success(request, 'Approved Successfully')

    listt=Non_approved.objects.filter(t_username=request.user.username)
    sign=1
    if len(listt) ==0:
        sign=0

    d=dict()
    d["name"]=request.user.first_name
    d["sign"]=sign
    d["listt"]=listt
    return render(request,'request.html',d)

#
# Teacher's Side |=> Detail page regarding the attendance in a course 
#


def details(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    if request.method=="POST":
        email_list=request.POST.get('Emailto')
        email_list=email_list.split(',')
        teacher_info=User.objects.filter(username=request.user.username)
        message=request.POST.get("message") +"\n \n Your Instructor," + "\n " + str(teacher_info[0].first_name) 
        title=request.POST.get("title")
        send_mail(
            title,
            message,
            'attendance.portal.1234@gmail.com',
            email_list,
            fail_silently=False,
        )
        messages.success(request,"Message Sent Successfully")
       

    return redirect('/insights')

#
# Teacher's Side |=> Page for Publishing the attendance of a course 
#

def publish(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    d=dict()
    if request.method=="POST":
        c_name=request.POST.get('Harry')
        d["name"]=request.user.first_name
        d["course"]=c_name
        return render(request,'publish.html',d)
    
    return redirect('/course')

#
# Teacher's Side |=> Detail page regarding Course, like students who are registered, their details,etc.
#

def course_details(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    d=dict()
    if request.method=="POST":
        c_name=request.POST.get('Harry')
        data=Approved.objects.filter(t_username=request.user.username,course_name=c_name)
        d["name"]=request.user.first_name
        d["course"]=c_name
        data_course=Course.objects.filter(username=request.user.username,course_name=c_name)
        d["join_code"]=data_course[0].join_code
        final_data=[]
        for i in data:
            dictionary=dict()
            object=Student_reg.objects.filter(username=i.s_username)
            dictionary["name"]=object[0].name 
            dictionary["id"]=i.s_id
            dictionary["user"]=i.s_username
            final_data.append(dictionary)

        d["data"]=final_data
        d["lendata"]=len(final_data)
        return render(request,'course_details.html',d)
    
    return redirect('/course')

#
# Teacher's Side |=> Post method function created to delete particular student in a course 
#

def del_student(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Teacher_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    d=dict()
    if request.method=="POST":
        user=request.POST.get('delete')
        user=user.split('+')
        if user[0] == "delete_all":
            li=Approved.objects.filter(t_username=request.user.username,course_name=user[1])
            object_report=Student_attendace_report.objects.filter(t_username=request.user.username,course_name=user[1])
            for i in object_report:
                f=i
                f.delete()
            count=0
            for i in range(0,len(li)):
                count+=1
                ob=li[i]
                ob.delete()
        elif user[0] == "!!!!":
            object1=Course.objects.filter(username=request.user.username,course_name=user[1])
            object2=Live.objects.filter(username=request.user.username,course_name=user[1])
            object3=Course_str.objects.filter(username=request.user.username,course_name=user[1])
            object4=Non_approved.objects.filter(t_username=request.user.username,course_name=user[1])
            object5=Approved.objects.filter(t_username=request.user.username,course_name=user[1])
            object6=Student_attendace_report.objects.filter(t_username=request.user.username,course_name=user[1])

            for i in object1:
                dup=i
                dup.delete()
            for i in object2:
                dup=i
                dup.delete()
            for i in object3:
                dup=i
                dup.delete()
            for i in object4:
                dup=i
                dup.delete()
            for i in object5:
                dup=i
                dup.delete()
            for i in object6:
                dup=i
                dup.delete()
            messages.success(request,"Course and all it's history has been deleted")
            return redirect('/course')
        else:
            list=Approved.objects.filter(t_username=request.user.username,s_username=user[0],course_name=user[1])
            if len(list)>0:
                list[0].delete()
            object_report=Student_attendace_report.objects.filter(t_username=request.user.username,s_username=user[0],course_name=user[1])
            if len(object_report) !=0:
                object_report[0].delete()

        messages.success(request,"Student/s Removed")
        return redirect('/course')
    
    return redirect('/course')



# # --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
#  Student Part Below  ||
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------

#
# Function for calculating the globe distabce between two points on Earth on the basis of latitudes and longitudes receieved from Geolocation Api.
#


def Calculate_globe_distance(a,b,c,d,radius):
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

#
# Student's Side |=> Student Home page and also MY accepted courses page
#

def stu(request): 
    
    d=dict()
    if(request.method=="POST"):
        if len(request.user.username) !=0:  
            hi=request.POST.get("krish")   
            hi=hi.split(',')
            objectt=Student_attendace_report.objects.filter(t_username=hi[0],s_username=request.user.username,course_name=hi[1],bool=0,time_present=int(hi[2]))
            objectt1=Student_attendace_report.objects.filter(t_username=hi[0],s_username=request.user.username,course_name=hi[1],bool=1,time_present=int(hi[2]))
            if len(objectt1) !=0:
                messages.success(request,"Attendance is already Marked")
            else:
                bool = int(hi[3])
                if bool == 1:
                    location=hi[7]
                    location=location.split('+')
                    if Calculate_globe_distance(float(hi[4]),float(location[0]),float(hi[5]),float(location[1]),float(hi[6])) == False:
                        messages.error(request,"Your Current Location is out of the range which instructor had set In. So please Go to Class to mark it.")
                        return redirect('/')

                
                val1=recognize(username=request.user.username,If_posted=0,Response_charge=0)
                count=0
                val1=recognize(username=request.user.username,If_posted=1,Response_charge=0)
                val1.save()
                val=recognize.objects.filter(username=request.user.username)
                while val[0].Response_charge == 0:
                    val=recognize.objects.filter(username=request.user.username)
                    count+=1

                val1=recognize(username=val[0].username,If_posted=0,Response_charge=0)
                val1.save()

                img1=cv2.imread('media/'+str(request.user.username)+'_imageno_0'+str(objectt[0].course_name)+'.jpg')
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
            val1=Join(username=username,If_posted=0,Response_charge=0,course_name="")
            val1.save()
            if User.objects.filter(username=username).exists():
                messages.error(request,"Account with the username already exists")
                return redirect('/')
            if User.objects.filter(email=email).exists():
                messages.error(request,"Account with the email already exists")
                return redirect('/')
            else:
                comma = ','
                if comma in email:
                    messages.error(request,"Email should not contain comma")
                    return redirect('/')
                con=Student_reg(name=name,email=email,username=username,password=password)
                con.save()
                user=User(username=username,email=email,password=password,first_name=name,last_name=name)
                user.save()
                if user is not None:
                    auth.login(request,user)
                    messages.success(request,"Registered Successfully")



    a=round(time.time() * 1000)
    g=Live.objects.exclude(time_future__lt=a)
    g1=Approved.objects.filter(s_username=request.user.username)
    final1=[]
    final2=[]
    for i in g1:
        for j in g:
            if (str(j.username)==str(i.t_username)) and (str(j.course_name) == str(i.course_name)):
                if j not in final1:
                    final1.append(j)
                if i not in final2:
                    final2.append(i)


    if(len(request.user.username)==0):
        return redirect('/')
    if Student_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')
    f=request.user.first_name 
    
    
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
    d["sign"]=sign
    return render(request,'stu_page.html',d)



#
# Student's Side |=> My Courses page
#

def my_course(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Student_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    d=dict()
    list=Approved.objects.filter(s_username=request.user.username) 
    d["name"]=request.user.first_name
    d["list"]=list
    d["Course_num"]=len(list)
    return render(request,'mycourses.html',d)


#
# Student's Side |=> Join a course page
#

def join(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Student_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')

    d=dict()
    if request.method=="POST":
        # c_name=request.POST.get('coursename')
        code=request.POST.get('code')
        id=request.POST.get('id')
        c_name=mapping.objects.filter(join_code=code)
        if len(c_name)==0:
            messages.error(request,"No Course found with the given join code. Please try again! ")
            return redirect('/')
        c_name=c_name[0].Course_name
        g=Course.objects.filter(course_name=c_name,join_code=code)
        g1=Non_approved.objects.filter(course_name=c_name,join_code=code,s_username=request.user.username)
        My_record=Approved.objects.filter(course_name=c_name,join_code=code,s_id=id)
        g2=Approved.objects.filter(course_name=c_name,join_code=code,s_username=request.user.username)
        
        if len(g1) !=0:
            messages.error(request,"Request to Instructor has already been sent by your account previously. ")
            return redirect('/')
        elif len(g2) !=0:
            messages.error(request,"You are already Registered ")
            return redirect('/')
        elif len(My_record) !=0:
            messages.error(request,"One student is already registered in the same course with the Id no. you provided.")
            return redirect('/')
       
        else:
            
            val1=Join(username=request.user.username,If_posted=0,Response_charge=0,course_name=c_name)
            count=0
            val1=Join(username=request.user.username,If_posted=1,Response_charge=0,course_name=c_name)
            val1.save()
            val=Join.objects.filter(username=request.user.username)
            while val[0].Response_charge == 0:
                val=Join.objects.filter(username=request.user.username)
                count+=1

            val1=Join(username=val[0].username,If_posted=0,Response_charge=0)
            val1.save()

            li=Teacher_reg.objects.filter(username=g[0].username)
            li2=Student_reg.objects.filter(username=request.user.username)
            st = request.user.username+'_imageno_0'
            img2=cv2.imread('media/'+str(request.user.username)+'_imageno_0'+str(c_name)+'.jpg')
            rgb_img2=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
            if( len(face_recognition.face_encodings(rgb_img2)) ==0):
                messages.error(request,"Please Try Again")
                return redirect('/')

            else:

                con=Non_approved(t_username=li[0].username,t_name=li[0].name,s_username=request.user.username,s_email=li2[0].email,s_id=id,course_name=c_name,img=st+str(c_name)+'.jpg',join_code=code)
                con.save()
                messages.success(request,"Request sent to respective Instructor Successfully ")
            return redirect('/')

    d["name"]=request.user.first_name
    messages.success(request,"Your image and Id no. will be processed to Instructor")
    return render(request,'join.html',d)

#
# Student's Side |=> Attendance Records page
#


def profile(request):
    if(len(request.user.username)==0):
        return redirect('/')
        
    if Student_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')
    
    
    d=dict()
    d["name"]=request.user.first_name
    all_attend=Course_str.objects.filter()
    list_of_my_Courses=[]
    final_list_of_courses=[]
    for i in range(0,len(all_attend)):
        object=all_attend[i]
        object1=Approved.objects.filter(s_username=request.user.username,course_name=object.course_name,t_username=object.username)
        count_attendance=0
        count_unattendance=0
        if len(object1)>0:
            dictionary=dict()
            teachname=Teacher_reg.objects.filter(username=object.username)
            dictionary["third"]=teachname[0].name
            dictionary["first"]=object
            given=object.attended_list
            given=given.split("!!!!")
            if request.user.email in given:
                dictionary["second"]=1
            else:
                dictionary["second"]=0
            
            final_list_of_courses.append(dictionary)
    
    final_list_of_courses.reverse()
    for i in final_list_of_courses:
        if i["second"] == 1:
            count_attendance += 1
        else:
            count_unattendance += 1

    d["final_list_of_courses"]=final_list_of_courses
    d["num"]=len(final_list_of_courses)
    d["count_attendance"]=count_attendance
    d["count_unattendance"]=count_unattendance
    return render(request,'profile.html',d)


#
# Common Routes
#

#
# Logout Post method for both Teacher ans student
#


def logout(request):
    user=request.user
    auth.logout(request)
    return redirect('/')


#
# Face Capturing Model in opencv, mediapipe and Harrcascade files for sudents joining a course. 
#


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
                    cv2.imwrite('media/'+str(request.user.username)+'_imageno_0'+str(val[0].course_name)+'.jpg', frame_flip)
                    val1=Join(username=val[0].username,If_posted=0,Response_charge=1,course_name=val[0].course_name)
                    val1.save()

        elif len(bboxs)>1:
            pass

        else:
            cv2.putText(frame_flip,'No face detected',(10, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),2,cv2.LINE_AA)
        
            # cv2.putText(frame_flip,'No face detected',(10, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),2,cv2.LINE_AA)

        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#
# Returns the output of above Method function to below function "Video_feed" to render it on Html Pages.
#


def video_feed(request):
    return StreamingHttpResponse(gen(request),content_type='multipart/x-mixed-replace; boundary=frame')


#
# Capturing as well as Recognizing Model of faces and Hands built in opencv, mediapipe and Harrcascade files for attending a class by the student. 
#


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



#
# Returns the output of above Method function to below function "Video_feed_1" to render it on Html Pages.
#

def video_feed_1(request):
    return StreamingHttpResponse(gen1(request),content_type='multipart/x-mixed-replace; boundary=frame')


