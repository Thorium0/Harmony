from django import forms
from .models import Friend_request, Message


class FriendRequestForm(forms.ModelForm):
    username = forms.CharField(max_length=30)

    class Meta:
        model = Friend_request
        fields = ['username']


class MessageForm(forms.ModelForm):

    text = forms.CharField(max_length=200, label=False)
    file = forms.FileField(required=False, label=False)

    class Meta:
        model = Message
        fields = ['text', 'file']
