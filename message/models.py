from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    user_1 = models.ForeignKey(User, related_name='user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='user_2', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)


class Friend_request(models.Model):
    requester = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE)
    requested = models.ForeignKey(User, related_name="requested", on_delete=models.CASCADE)
    sent_on = models.DateTimeField(auto_now=True)
    


class Conversation(models.Model):
    of_friends = models.OneToOneField(Friend, on_delete=models.CASCADE)



class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    sent_on = models.DateTimeField(auto_now=True)