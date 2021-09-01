from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
import json
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse


def main(request):
    return redirect("account/login")


def main(request):
    return redirect("account/login")

def signup(request):
    if request.method == 'GET':
        return render(request,'account/signup.html', {
            'signupForm': CreateUserForm(),
        })
    else:
        createUserForm = CreateUserForm(request.POST)
        if createUserForm.is_valid():
            createUserForm.save()
        return redirect("account/login")

def login(request):
    if request.method == 'GET':
        return render(request, "account/login.html",{
            'loginForm' : LoginForm()
        })
    else:
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            userId = loginForm.cleaned_data["username"]
            password = loginForm.cleaned_data["password"]
            user = authenticate(userId=userId, password=password)
            if user:
                user.loginCount = 5
                save_session(request, userId, password)
                user.save()
                return redirect("/parent/main")
            else :
                user = User.objects.get(userId = loginForm.cleaned_data["username"])
                if user.loginCount == 0:
                    user.is_active = 0
                else:
                    user.loginCount = user.loginCount -1
                user.save()
                return render(request, "account/login.html",{
                    'loginForm' : LoginForm(),
                    'loginCount' : user.loginCount,
                })
        else:
            return 0

def save_session(request,userId,password):
    request.session["userId"] =userId
    request.session["password"] = password
