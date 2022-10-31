from django.contrib import admin
from .models import Message, Friend, Friend_request

admin.site.register([Message, Friend, Friend_request])
