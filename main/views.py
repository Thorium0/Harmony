from http.client import HTTPResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from message.models import Friend_request, Friend
from django.http import JsonResponse
import datetime



@login_required
def update(request, loaded_on):
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

    messages = []
    
    data["messages"] = messages
    
    return JsonResponse(data)



@login_required
def friends(request):
    friend_requests = Friend_request.objects.filter(requested=request.user)
    friends = []
    for friend in Friend.objects.filter(user_1=request.user):
        friends.append(friend.user_2)
    for friend in Friend.objects.filter(user_2=request.user):
        friends.append(friend.user_1)



    if request.method == 'POST':
        pass
    else:
        pass

    
    context = {
    "title" : "Friends",
    "requests": friend_requests,
    "friends": list(friends)
    }
    return render(request, 'main/friends.html.django', context)