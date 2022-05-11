from atexit import register
from django.contrib import admin
from home.models import contact
from home.models import Mains
# Register your models here.
admin.site.register(contact)
admin.site.register(Mains)