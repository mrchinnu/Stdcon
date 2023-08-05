from django.contrib import admin

# Register your models here.

from .models import Chatroom,Messages,Topic

admin.site.register(Chatroom)
admin.site.register(Messages)
admin.site.register(Topic)