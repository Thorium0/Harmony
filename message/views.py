from django.shortcuts import render, redirect
from .models import Friend, Friend_request, Server, Server_link, Server_message
from .forms import FriendRequestForm, ServerMessageForm, JoinServerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import datetime, sys, time



def getMessagesFromServer(server, time=False):
    if time:
        text_messages = Server_message.objects.filter(server=server, sent_on__gt=time)
    else:
        text_messages = Server_message.objects.filter(server=server)
    return text_messages
    



@login_required
def server_update(request, loaded_on, server_id):
    data = {}
    time = datetime.datetime.strptime(loaded_on, "%Y-%m-%d_%H:%M:%S.%f")



    servers = []
    message_list = []
    if server_id != 0:
    
        server = Server.objects.get(id=server_id)
        messages = getMessagesFromServer(server, time=loaded_on)
        for message in messages:
            if message.file:
                short_name = message.file.name.replace("files/", "")
                message_list.append({"username": message.sender.username, "image_url": message.sender.profile.image.url, "message_text": message.text, "sent_on": message.sent_on, "file_path": message.file.url, "file_name": short_name})
            else:
                message_list.append({"username": message.sender.username, "image_url": message.sender.profile.image.url, "message_text": message.text, "sent_on": message.sent_on})
    
    
            
    data["servers"] = servers
    data["messages"] = message_list
    data["new_time"] = str(datetime.datetime.now())
    return JsonResponse(data)





@login_required
def add_friend(request):
    if request.method == 'POST':
        form = FriendRequestForm(request.POST)

        if form.is_valid():
            friend_request = form.save(commit=False)
            friend_request.requester = request.user

            
            username = form.cleaned_data.get("username")
            try: friend_request.requested = User.objects.get(username=username)
            except:
                messages.warning(request, "User not found")
                return redirect('add_friend')


            try: Friend_request.objects.get(requester=request.user, requested=friend_request.requested)
            except: pass
            else:
                messages.warning(request, "You have already sent a request to this user")
                return redirect('add_friend')


            try: Friend.objects.get(user_1=request.user, user_2=friend_request.requested)
            except: pass
            else: 
                messages.warning(request, "You are already friends")
                return redirect('add_friend')
            try: Friend.objects.get(user_2=request.user, user_1=friend_request.requested)
            except: pass
            else: 
                messages.warning(request, "You are already friends")
                return redirect('add_friend')

            

            if (friend_request.requester == friend_request.requested):
                messages.warning(request, "Can't add yourself as a friend, you loner..")
                return redirect('add_friend')
            
            try: friend_request.save()
            except: 
                messages.error(request, "Error")
            else: 
                messages.success(request, "Friend request sent!")
                return redirect('friends')


    else:
        form = FriendRequestForm()
    context = {
    'title': "Add friend",
    'form': form
    }
    return render(request, 'message/add_friend.html.django', context)


@login_required
def finalize_friend(request, id):
    friend_request = Friend_request.objects.get(id=id)
    user_1 = friend_request.requester
    user_2 = friend_request.requested

    if friend_request.requested != request.user:
        return redirect('friends')

    try: Friend.objects.get(user_1=user_1, user_2=user_2)
    except: pass
    else: return redirect('remove_friend_request', id)
    try: Friend.objects.get(user_2=user_1, user_1=user_2)
    except: pass
    else: return redirect('remove_friend_request', id)


    try: friend = Friend.objects.create(user_1=user_1, user_2=user_2)
    except: 
        messages.error(request, "Error adding friend")
        return redirect('friends')
    else: 
        messages.success(request, "Success in adding friend")
        return redirecjoin_servert('remove_friend_request', id)



@login_required
def remove_request(request, id):
    friend_request = Friend_request.objects.get(id=id)
    if friend_request.requested != request.user:
        return redirect('friends')

    try: friend_request.delete()
    except: messages.error(request, "Error removing request")
    
    return redirect('friends')




@login_required
def join_server(request):
    if request.method == 'POST':
        form = JoinServerForm(request.POST)

        if form.is_valid():
            server_link = form.save(commit=False)
            server_link.user = request.user

            
            name = form.cleaned_data.get("name")
            try: server = Server.objects.get(name=name)
            except: 
                Server.objects.create(name=name)
                server = Server.objects.get(name=name)

            server_link.server = server


            try: Server_link.objects.get(server=server, user=request.user)
            except: pass
            else: 
                messages.warning(request, "You are already in this server")
                return redirect('join_server')
          
            
            try: server_link.save()
            except: 
                messages.error(request, "Error")
            else: 
                messages.success(request, "Server joined!")
                return redirect('servers')


    else:
        form = JoinServerForm()
    context = {
    'title': "Join server",
    'form': form
    }
    return render(request, 'message/join_server.html.django', context)



@login_required
def servers(request):
    servers = []
    for link in Server_link.objects.filter(user=request.user):
        servers.append(link.server)



    loaded_on = datetime.datetime.now()
    
    context = {
    "title" : "Servers",
    "servers": servers,
    "loaded_on": str(loaded_on)
    }
    return render(request, 'message/servers.html.django', context)




@login_required
def server_select(request, server_name):
    servers = []
    for link in Server_link.objects.filter(user=request.user):
        servers.append(link.server)

    

    try: selected_server = Server.objects.get(name=server_name)
    except: return redirect("servers")
    text_messages = []

    if request.method == 'POST':
        form = ServerMessageForm(request.POST, request.FILES)

        if form.is_valid():
            message = form.save(commit=False)

            message.sender = request.user
            message.server = selected_server

            form.save()
            return redirect("server_select", server_name)

    else:
        form = ServerMessageForm()
        text_messages = getMessagesFromServer(selected_server)
        for msg in text_messages:
            if 'win' in sys.platform:
                msg.sent_on = msg.sent_on.strftime("%b %#dth %Y, %H:%M:%S")
            else:
                msg.sent_on = msg.sent_on.strftime("%b %-dth %Y, %H:%M:%S")
            msg.file.short_name = msg.file.name.replace("files/", "")


    loaded_on = datetime.datetime.now()
    server_info = {}
    server_info["name"] = selected_server.name
    server_info["id"] = selected_server.id

    
    context = {
    "title" : "Servers",
    "servers": servers,
    "form": form,
    "text_messages": text_messages,
    "server_info": server_info,
    "loaded_on": str(loaded_on)
    }
    return render(request, 'message/server_select.html.django', context)



@login_required
def server_call(request, server_id):


    
    server = Server.objects.get(id=server_id)


    appId = "95c5b44bf3be4174b77904ef6a625ee6"
    appCertificate = "e56b921b7e3648329e194e0bf9ad0d11"
    channelName = server.name.__str__().replace(" ","")
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
    "channel_name": channelName,
    "server_name": server.name
    }
    return render(request, 'message/call_server.html.django', context)