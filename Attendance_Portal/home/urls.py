from django.contrib import admin
from django.urls import path
from home import views

#
# Url's for all the paths routedin project
#

urlpatterns = [
    path('',views.index, name='home'),
    path('teacher_page',views.teach, name='teach'),
    path('student_page',views.stu, name='stu'),
    path('create',views.create, name='create'),
    path('my_course',views.my_course, name='my_course'),
    path('course',views.course, name='course'),
    path('Request',views.Request, name='Request'),
    path('insights',views.insights, name='insights'),
    path('join',views.join, name='join'),
    path('profile',views.profile, name='profile'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('video_feed_1', views.video_feed_1, name='video_feed_1'),
    # path('saveimage',views.saveimage, name='saveimage').
    path('details', views.details, name='details'),
    path('publish',views.publish, name='publish'),
    path('course_details',views.course_details, name='course_details'),
    path('del_student',views.del_student, name='del_student'),
    path('logout',views.logout, name='logout')
]

