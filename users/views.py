from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login as UserLogin
from django.contrib.auth import views as auth_views
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout as DjangoLogout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            UserLogin(request, user)
            messages.success(request, f'Account "{username}" Created Successfully!')
            try: next_page = request.GET['next']
            except: return redirect('friends')
            else: return HttpResponseRedirect(next_page)

    else:
        form = UserRegisterForm()

    context = {
    'title': "Register",
    'form': form
    }
    return render(request, 'users/register.html.django', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        username = form.data["username"]
        password = form.data["password"]
        user = authenticate(
            request=request,
            username=username,
            password=password
        )
        if user is not None:
            UserLogin(request, user)
        try: next_page = request.GET['next']
        except: return redirect('home')
        else: return HttpResponseRedirect(next_page)

    else:
        form = AuthenticationForm()

    context = {
    'title': "Login",
    'form': form
    }
    return render(request, 'users/login.html.django', context)


@login_required
def logout(request):
    DjangoLogout(request)
    return redirect("friends")


@login_required
def profile(request):
    if request.method == 'POST':
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, 'Your Profile has Been Updated!')
            return redirect('profile')

    else:
        userForm = UserUpdateForm(instance=request.user)
        if request.user.profile.image.name == 'default-profile.jpg':
            profileForm = ProfileUpdateForm()
        else:
            profileForm = ProfileUpdateForm(instance=request.user.profile)

    context = {
    'title': request.user.username+"'s Profile",
    'userForm': userForm,
    'profileForm': profileForm
    }
    return render(request, 'users/profile.html.django', context)



@login_required
def changePassword(request):
    if request.method == 'POST':
        passwordForm = PasswordChangeForm(request.user, request.POST)
        if passwordForm.is_valid():
            user = passwordForm.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        passwordForm = PasswordChangeForm(request.user)

    context = {
    'title': "Change Password",
    'passwordForm': passwordForm
    }
    return render(request, 'users/changepassword.html.django', context)
