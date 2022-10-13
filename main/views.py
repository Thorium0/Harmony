from django.shortcuts import render
from django.core.files.storage import default_storage


def friends(request):
    
    context = {
    "title" : "Friends",
    }
    return render(request, 'main/friends.html.django', context)