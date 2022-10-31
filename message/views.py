from django.shortcuts import render, redirect
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
            friend_request.sender = request.user

            
            username = form.cleaned_data.get("username")
            try: friend_request.receiver = User.objects.get(username=username)
            except:
                messages.warning(request, "User not found")
                return redirect('add_friend')

            

            if (friend_request.sender == friend_request.receiver):
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
    messages.success(request, "id is"+id)
    return redirect('friends')



@login_required
def remove_request(request, id):
    messages.success(request, "id is"+id)
    return redirect('friends')
