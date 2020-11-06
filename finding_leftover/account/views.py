from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

from .forms import UserCreationMultiForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

from store.models import Store

def signup(request):
    # signup 으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
    if request.method == 'POST':
        signup_form = UserCreationMultiForm(request.POST, request.FILES) 

        if signup_form.is_valid():
            user = signup_form['user'].save()  # user 저장하고
            store = signup_form['store'].save(commit=False)
            store.user=user                     # store랑 user를 연결
            
            # 주소저장
            store.store_address = request.POST.get('address') + request.POST.get('detailAddress') + request.POST.get('extraAddress')
            store.store_local = (request.POST.get('local'))
            
            store.save()                        # store를 저장
            auth.login(request, user)
            return redirect('home')

    # signup으로 GET 요청이 왔을 때, 회원가입 화면을 띄워준다.
    else:
        signup_form = UserCreationMultiForm()
    return render(request, 'signup.html', {'signup_form':signup_form})


def login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
        else:
            return render(request, 'error.html')
        return redirect('home')
    else:
        login_form = AuthenticationForm()
    
    return render(request, 'login.html', {'login_form' : login_form})



# 로그 아웃
def logout(request):
    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

    # logout으로 GET 요청이 들어왔을 때, 로그인 화면을 띄워준다.
    return render(request, 'logout.html')
