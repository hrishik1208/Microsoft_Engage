from atexit import register
from django.contrib import admin
from home.models import contact
from home.models import Mains
from home.models import Student_reg
from home.models import Teacher_reg
from home.models import Course
from home.models import Live
from home.models import Course_str
from home.models import Non_approved
from home.models import Approved
from home.models import Student_attendace_report
# Register your models here.
admin.site.register(contact)
admin.site.register(Mains)
admin.site.register(Teacher_reg)
admin.site.register(Student_reg)
admin.site.register(Course)
admin.site.register(Live)
admin.site.register(Course_str)
admin.site.register(Non_approved)
admin.site.register(Approved)
admin.site.register(Student_attendace_report)