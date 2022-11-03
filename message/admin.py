from django.contrib import admin
from .models import Message, Friend, Friend_request, Conversation

admin.site.register([Conversation, Message, Friend, Friend_request])
