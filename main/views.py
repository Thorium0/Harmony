from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from message.models import Friend_request, Friend, Message, Conversation, Server
from message.forms import MessageForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import datetime, sys, time



def getMessagesFromUser(request, friend_user, time=False):
    try: friend_link = Friend.objects.get(user_1=request.user, user_2=friend_user)
    except: friend_link = Friend.objects.get(user_2=request.user, user_1=friend_user)
    try: conversation = Conversation.objects.get(of_friends=friend_link)
    except: 
        Conversation.objects.create(of_friends=friend_link)
        conversation = Conversation.objects.get(of_friends=friend_link)
    else:
        if time:
            text_messages = Message.objects.filter(conversation=conversation, sent_on__gt=time)
        else:
            text_messages = Message.objects.filter(conversation=conversation)
    return text_messages
    


@login_required
def update(request, loaded_on, user_id):
    data = {}
    time = datetime.datetime.strptime(loaded_on, "%Y-%m-%d_%H:%M:%S.%f")

    friends = []
    for friend in Friend.objects.filter(user_1=request.user, created_on__gt=time):
        friends.append({"user_id": friend.user_2.id, "username":friend.user_2.username, "image_url": friend.user_2.profile.image.url})
    for friend in Friend.objects.filter(user_2=request.user, created_on__gt=time):
        friends.append({"user_id": friend.user_1.id, "username":friend.user_1.username, "image_url": friend.user_1.profile.image.url})
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
            if message.file:
                short_name = message.file.name.replace("files/", "")
                message_list.append({"username": friend_user.username, "image_url": friend_user.profile.image.url, "message_text": message.text, "sent_on": message.sent_on, "file_path": message.file.url, "file_name": short_name})
            else:
                message_list.append({"username": friend_user.username, "image_url": friend_user.profile.image.url, "message_text": message.text, "sent_on": message.sent_on})

            
    
    data["messages"] = message_list
    data["new_time"] = str(datetime.datetime.now())
    return JsonResponse(data)



@login_required
def friends(request):
    friend_requests = Friend_request.objects.filter(requested=request.user)
    friends = []
    for friend in Friend.objects.filter(user_1=request.user):
        friends.append(friend.user_2)
    for friend in Friend.objects.filter(user_2=request.user):
        friends.append(friend.user_1)


    loaded_on = datetime.datetime.now()
    
    context = {
    "title" : "Friends",
    "requests": friend_requests,
    "friends": friends,
    "loaded_on": str(loaded_on)
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

    
    text_messages = []

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)

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
        text_messages = getMessagesFromUser(request, friend_user)
        for msg in text_messages:
            if 'win' in sys.platform:
                msg.sent_on = msg.sent_on.strftime("%b %#dth %Y, %H:%M:%S")
            else:
                msg.sent_on = msg.sent_on.strftime("%b %-dth %Y, %H:%M:%S")
            msg.file.short_name = msg.file.name.replace("files/", "")


    loaded_on = datetime.datetime.now()
    user_info = {}
    friend_user = User.objects.get(id=user_id)
    user_info["username"] = friend_user.username
    user_info["image_url"] = friend_user.profile.image.url
    user_info["id"] = user_id

    
    context = {
    "title" : "Friends",
    "requests": friend_requests,
    "friends": friends,
    "form": form,
    "text_messages": text_messages,
    "user_info": user_info,
    "loaded_on": str(loaded_on)
    }
    return render(request, 'main/friend_select.html.django', context)


@login_required
def call(request, user_id):


    friend_user = User.objects.get(id=user_id)
    try: friend_link = Friend.objects.get(user_1=request.user, user_2=friend_user)
    except: friend_link = Friend.objects.get(user_2=request.user, user_1=friend_user)
    
    conversation = Conversation.objects.get(of_friends=friend_link)


    appId = "95c5b44bf3be4174b77904ef6a625ee6"
    appCertificate = "e56b921b7e3648329e194e0bf9ad0d11"
    channelName = conversation.__str__().replace(" ","")
    uid = 0
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)


    context = {
    "title" : "Friends",
    "user_id": request.user.id,
    'token': token, 
    'app_id': appId,
    'uid': uid,
    "channel_name": channelName
    }
    return render(request, 'main/call.html.django', context)


@login_required
def call_server(request, server_id):


    server = Server.objects.get(id=server_id)


    appId = "95c5b44bf3be4174b77904ef6a625ee6"
    appCertificate = "e56b921b7e3648329e194e0bf9ad0d11"
    channelName = server.__str__().replace(" ","")
    uid = 0
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)


    context = {
    "title" : "Friends",
    "user_id": server_id,
    'token': token, 
    'app_id': appId,
    'uid': uid,
    "channel_name": channelName
    }
    return render(request, 'main/call.html.django', context)


