from django.shortcuts import render
from django.contrib.auth.models import User
from Login_app.models import UserInfo
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from  django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



from Login_app.registration import UserInfoForm, UserForm

# Create your views here.

def Index(request):
    diction = {}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk = user_id)
        user_more_info = UserInfo.objects.get(user__pk = user_id)
        diction = {
            'user_basic_info' : user_basic_info,
            'user_more_info' : user_more_info
        }
    return render(request, 'Login_app/index.html', context=diction)

def Registration(request):
    register = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            userinfo = user_info_form.save(commit=False)
            userinfo.user = user

            if 'profile_pic' in request.FILES:
                userinfo.profile_pic = request.FILES['profile_pic']
            
            userinfo.save()
            register = True
    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()
    diction = {'userinfo': user_form, 'usermoreinfo': user_info_form, 'registration': register}
    return render(request, 'Login_app/registration_form.html', context=diction)


def Login_page(request):
    return render(request, 'Login_app/login_form.html', context={})

def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        user_password = request.POST.get('password')
        print(user_name)
        print(user_password)
        user = authenticate(username = user_name, password = user_password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Login_app:index'))
            else:
                return HttpResponse("User not active")
        else:
            return HttpResponse("Invalid username and password")
    else:
        return HttpResponseRedirect(reverse('Login_app:login')) 

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_app:login'))