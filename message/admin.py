from django.contrib import admin
from .models import Message, Friend, Friend_request, Server, Server_message

admin.site.register([Message, Friend, Friend_request, Server, Server_message])
