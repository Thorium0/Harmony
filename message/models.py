from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    sent_on = models.DateTimeField(auto_now=True)


class Friend(models.Model):
    user_1 = models.ForeignKey(User, related_name='user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='user_2', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)



class Friend_request(Message):
    pass
    