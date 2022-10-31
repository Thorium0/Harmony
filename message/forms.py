from django import forms
from django.contrib.auth.models import User
from .models import Friend_request


class FriendRequestForm(forms.ModelForm):
    username = forms.CharField(max_length=30)

    class Meta:
        model = Friend_request
        fields = ['username']
