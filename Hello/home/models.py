from tkinter import Image
from unicodedata import name
from django.db import models
from datetime import datetime
import os

from django.forms import ImageField
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

class Mains(models.Model):
    name=models.CharField(max_length=100,default="kshh")
    img=models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name