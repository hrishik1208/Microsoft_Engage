from io import SEEK_END
from pickle import TRUE
from re import S
from reprlib import aRepr
from xmlrpc.client import TRANSPORT_ERROR
from cv2 import idct
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
import datetime
from home.models import contact
from home.models import Mains
from home.models import Teacher_reg
from home.models import Student_reg
from home.models import Course
from home.models import Live
from home.models import Course_str
from home.models import Non_approved
from home.models import Approved
from django.contrib import messages
from django.contrib.auth.models import User,auth
import cv2
import face_recognition
import time
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
            a=round(time.time() * 1000)
            print(a)
            a=a+((Time*60)*1000)
            m1=Live(username=request.user.username,course_name=c_name,time_future=a,attended_list="")
            m1.save()
            hi=datetime.date.today()
            gi=0
            m2=Course_str(username=request.user.username,course_name=c_name,date=hi,attended_list="")
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



def stu(request): 
    
    d=dict()
    if(request.method=="POST"):
        
        name=request.POST.get('name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
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
        d["name"]=name 
        return render(request,'stu_page.html',d) 

    g=Live.objects.filter()
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
    a=round(time.time() * 1000)
    print("lenght ",len(final1))
    sign=1
    for i in range(0,len(final1)):
        if final1[i].time_future <=a :
            d=final1[i]
            d.delete()

    d["final"]=[]
    if len(final1)==0:
        sign=0
    else:
        d["final1"]=final1[0]
        
    d["name"]=f
    d["list"]=list
    
    # print("lenght ",len(final1))
    d["sign"]=sign
    return render(request,'stu_page.html',d)

def join(request):
    if(len(request.user.username)==0):
        return redirect('/')

    if Student_reg.objects.filter(username=request.user.username).exists() == False :
        return redirect('/')
        
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
            li=Teacher_reg.objects.filter(username=g[0].username)
            li2=Student_reg.objects.filter(username=request.user.username)
            run(str(request.user.username)+str(li[0].username))
            print("This ihiowhuowhon",str(request.user.username)+str(li[0].username)+".jpg")
            con=Non_approved(t_username=li[0].username,t_name=li[0].name,s_username=request.user.username,s_email=li2[0].email,s_id=id,course_name=c_name,img=str(request.user.username)+str(li[0].username)+".jpg",join_code=code)
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

  
    
    