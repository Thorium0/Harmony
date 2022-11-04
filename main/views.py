from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from message.models import Friend_request, Friend, Message, Conversation
from message.forms import MessageForm
from django.contrib.auth.models import User
from django.http import JsonResponse
import datetime



def getMessagesFromUser(request, friend_user, time=False):
    try: friend_link = Friend.objects.get(user_1=request.user, user_2=friend_user)
    except: friend_link = Friend.objects.get(user_2=request.user, user_1=friend_user)

    form = MessageForm()
    try: conversation = Conversation.objects.get(of_friends=friend_link)
    except: pass
    else:
        if time:
            messages = Message.objects.filter(conversation=conversation, sent_on__gt=time)
        else:
            messages = Message.objects.filter(conversation=conversation)
    return messages
    


@login_required
def update(request, loaded_on, user_id):
    data = {}
    time = datetime.datetime.strptime(loaded_on, '%Y-%m-%d_%H:%M:%S')

    friends = []
    for friend in Friend.objects.filter(user_1=request.user, created_on__gt=time):
        friends.append({"conv_id": friend.id, "username":friend.user_2.username, "image_url": friend.user_2.profile.image.url})
    for friend in Friend.objects.filter(user_2=request.user, created_on__gt=time):
        friends.append({"id": friend.id, "username":friend.user_1.username, "image_url": friend.user_1.profile.image.url})
    data["friends"] = friends
        
    friend_requests = Friend_request.objects.filter(requested=request.user, sent_on__gt=time)
    requests = []
    for friend_request in friend_requests:
        requests.append({"request_id": friend_request.id, "username": friend_request.requester.username, "image_url": friend_request.requester.profile.image.url})
    data["friend_requests"] = requests

    message_list = []
    if user_id != 0:
        friend_user = User.objects.get(id=user_id)
        messages = getMessagesFromUser(request, friend_user, time=loaded_on)
        for message in messages:
            message_list.append({"username": friend_user.username, "image_url": friend_user.profile.image.url, "message_text": message.text})
    
    data["messages"] = message_list
    
    return JsonResponse(data)



@login_required
def friends(request):
    friend_requests = Friend_request.objects.filter(requested=request.user)
    friends = []
    for friend in Friend.objects.filter(user_1=request.user):
        friends.append(friend.user_2)
    for friend in Friend.objects.filter(user_2=request.user):
        friends.append(friend.user_1)
    
    context = {
    "title" : "Friends",
    "requests": friend_requests,
    "friends": friends
    }
    return render(request, 'main/friends.html.django', context)




@login_required
def friend_select(request, user_id):
    friend_requests = Friend_request.objects.filter(requested=request.user)
    friends = []
    for friend in Friend.objects.filter(user_1=request.user):
        friends.append(friend.user_2)
    for friend in Friend.objects.filter(user_2=request.user):
        friends.append(friend.user_1)

    
    messages = []

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)

            friend_user = User.objects.get(id=user_id)
            try: friend_link = Friend.objects.get(user_1=request.user, user_2=friend_user)
            except: friend_link = Friend.objects.get(user_2=request.user, user_1=friend_user)

            try: conversation = Conversation.objects.get(of_friends=friend_link)
            except:
                Conversation.objects.create(of_friends=friend_link)
                conversation = Conversation.objects.get(of_friends=friend_link)
            
            message.conversation = conversation
            message.sender = request.user

            form.save()
            return redirect("friend_select", user_id)

    else:
        form = MessageForm()
        friend_user = User.objects.get(id=user_id)
        messages = getMessagesFromUser(request, friend_user)
    
    context = {
    "title" : "Friends",
    "requests": friend_requests,
    "friends": friends,
    "form": form,
    "text_messages": messages,
    "user_id": user_id
    }
    return render(request, 'main/friend_select.html.django', context)