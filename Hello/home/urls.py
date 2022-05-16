from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('',views.index, name='home'),
    path('teacher_page',views.teach, name='teach'),
    path('student_page',views.stu, name='stu'),
    path('create',views.create, name='create'),
    path('course',views.course, name='course'),
    path('Request',views.Request, name='Request'),
    path('insights',views.insights, name='insights'),
    path('join',views.join, name='join'),
    path('profile',views.profile, name='profile'),
    # path('saveimage',views.saveimage, name='saveimage').
    path('cam',views.cam, name='cam'),
    path('logout',views.logout, name='logout')
]
