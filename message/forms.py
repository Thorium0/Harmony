from django import forms
from emoji_picker.widgets import EmojiPickerTextInputAdmin
from .models import Friend_request, Message, Server_message, Server_link

class FriendRequestForm(forms.ModelForm):
    username = forms.CharField(max_length=30)

    class Meta:
        model = Friend_request
        fields = ['username']


class MessageForm(forms.ModelForm):

    text = forms.CharField(widget=EmojiPickerTextInputAdmin, max_length=200, label=False)
    file = forms.FileField(required=False, label=False)

    class Meta:
        model = Message
        fields = ['text', 'file']


class JoinServerForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label="Server name")
    class Meta:
        model = Server_link
        fields = ['name']


class ServerMessageForm(forms.ModelForm):

    text = forms.CharField(widget=EmojiPickerTextInputAdmin, max_length=200, label=False)
    file = forms.FileField(required=False, label=False)

    class Meta:
        model = Server_message
        fields = ['text', 'file']
