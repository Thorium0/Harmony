from django.shortcuts import render
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from message.models import Friend_request, Friend


@login_required
def friends(request):
    friend_requests = Friend_request.objects.filter(receiver=request.user)
    friends = []
    for friend in Friend.objects.filter(user_1=request.user):
        friends.append(friend.user_2)
    for friend in Friend.objects.filter(user_2=request.user):
        friends.append(friend.user_1)
    context = {
    "title" : "Friends",
    "requests": friend_requests,
    "friends": list(friends)
    }
    return render(request, 'main/friends.html.django', context)