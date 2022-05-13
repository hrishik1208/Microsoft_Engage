from atexit import register
from django.contrib import admin
from home.models import contact
from home.models import Mains
from home.models import Student_reg
from home.models import Teacher_reg
# Register your models here.
admin.site.register(contact)
admin.site.register(Mains)
admin.site.register(Teacher_reg)
admin.site.register(Student_reg)