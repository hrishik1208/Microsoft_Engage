from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('',views.index, name='home'),
    path('teacher_page',views.teach, name='teach'),
    path('student_page',views.stu, name='stu'),
    # path('saveimage',views.saveimage, name='saveimage').
    path('cam',views.cam, name='cam')
]
