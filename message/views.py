from django.shortcuts import render, redirect

from message.models import Friend, Friend_request, Message
from .forms import FriendRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

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
    'title': "Login",
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
        return redirect('remove_friend_request', id)



@login_required
def remove_request(request, id):
    friend_request = Friend_request.objects.get(id=id)
    if friend_request.requested != request.user:
        return redirect('friends')

    try: friend_request.delete()
    except: messages.error(request, "Error removing request")
    
    return redirect('friends')
