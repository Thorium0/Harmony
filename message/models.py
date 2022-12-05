from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Friend(models.Model):
    user_1 = models.ForeignKey(User, related_name='user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='user_2', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_1.username} - {self.user_2.username}'


class Friend_request(models.Model):
    requester = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE)
    requested = models.ForeignKey(User, related_name="requested", on_delete=models.CASCADE)
    sent_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.requester.username} > {self.requested.username}'
    


class Conversation(models.Model):
    of_friends = models.OneToOneField(Friend, on_delete=models.CASCADE)

    def __str__(self):
        return self.of_friends.__str__()



class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.CharField(max_length=400)
    sent_on = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return f'{self.sender}: {self.text}'





class Server(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Server_link(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Server_message(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=400)
    sent_on = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='files/')



