from pyexpat import model
from tkinter import Image
from unicodedata import name
from django.db import models
from datetime import datetime
import os

from django.forms import ImageField, IntegerField
# Create your models here.
class contact(models.Model):
    name=models.CharField(max_length=100,default="kshh")
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    # date=models.DateField()
    # check=models.CharField()

    def __str__(self):
        return self.name
class Teacher_reg(models.Model):
    name=models.CharField(max_length=100,default="kshh")
    username=models.CharField(max_length=100,default="kshh")
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    # date=models.DateField()
    # check=models.CharField()

    def __str__(self):
        return self.name

class Student_reg(models.Model):
    name=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    # date=models.DateField()
    # check=models.CharField()

    def __str__(self):
        return self.name

class Course(models.Model): 
    username=models.CharField(max_length=100) 
    course_name=models.CharField(max_length=100) 
    join_code=models.CharField(max_length=100) 
    # date=models.DateField()
    # check=models.CharField()

    def __str__(self):
        return self.course_name


class Live(models.Model):
    username=models.CharField(max_length=100)
    course_name=models.CharField(max_length=100)
    time_future=models.IntegerField()
    time_present=models.IntegerField(default=0)
    attended_list=models.TextField(null=True)
    date=models.DateField(default="2021-10-10")
    latitude=models.DecimalField(max_digits=19,decimal_places=15,default=0)
    longitude=models.DecimalField(max_digits=19,decimal_places=15,default=0)
    bool = models.IntegerField(default=0)
    radius = models.IntegerField(default=0,)
    # date=models.DateField()
    # check=models.CharField()
    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.course_name

class Course_str(models.Model):
    username=models.CharField(max_length=100)
    course_name=models.CharField(max_length=100)
    date=models.DateField(default="2021-10-10")
    time_present=models.IntegerField(default=0)
    attended_list=models.TextField(null=True)
    class Meta:
        ordering = ('time_present',)
    
    def __str__(self):
        return self.course_name

class Non_approved(models.Model):
    t_username=models.CharField(max_length=100)
    t_name=models.CharField(max_length=100)
    s_username=models.CharField(max_length=100)
    s_id=models.IntegerField(default="10000000")
    s_email=models.CharField(max_length=100)
    course_name=models.CharField(max_length=100)
    img=models.ImageField(null=True,blank=True)
    join_code=models.CharField(max_length=100) 

    def __str__(self):
        return self.course_name

class Approved(models.Model):
    t_username=models.CharField(max_length=100)
    t_name=models.CharField(max_length=100)
    s_username=models.CharField(max_length=100)
    s_id=models.IntegerField(default="10000000")
    s_email=models.CharField(max_length=100)
    course_name=models.CharField(max_length=100)
    img=models.ImageField(null=True,blank=True)
    join_code=models.CharField(max_length=100) 

    def __str__(self):
        return self.course_name


class Student_attendace_report(models.Model):
    t_username=models.CharField(max_length=100)
    s_username=models.CharField(max_length=100)
    course_name=models.CharField(max_length=100)
    date=models.DateField(default="2021-10-10")
    bool=models.IntegerField(default=0)
    time_present=models.IntegerField()

    class Meta:
        ordering = ('time_present',)

    def __str__(self):
        return self.course_name

class Join(models.Model):
    username=models.CharField(max_length=100,primary_key=True)
    If_posted=models.IntegerField(default=0)
    Response_charge=models.IntegerField(default=0)

class recognize(models.Model):
    username=models.CharField(max_length=100,primary_key=True)
    If_posted=models.IntegerField(default=0)
    Response_charge=models.IntegerField(default=0)

class Mains(models.Model):
    name=models.CharField(max_length=100,default="kshh")
    img=models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name
 