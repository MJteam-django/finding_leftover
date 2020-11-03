from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

from .forms import UserCreationMultiForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

from post.models import Store
"""
#회원 가입 완
def signup(request):
    # signup 으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
    if request.method == 'POST':
        # password와 confirm에 입력된 값이 같다면
        if request.POST['password'] == request.POST['confirm']:
            # user 객체를 새로 생성
            user = User.objects.create_user(
                username=request.POST['username'], 
                password=request.POST['password'], 
                )
            store_name = request.POST.get("store_name","")
            store_address = request.POST['store_address']
            store_memo = request.POST['store_memo']
            store_image = request.FILES['store_image']
            store = Store(user=user, store_name=store_name, store_address=store_address, store_memo=store_memo, store_image=store_image)
            store.save()
            # 로그인 한다
            auth.login(request, user)
            return redirect('home')
    # signup으로 GET 요청이 왔을 때, 회원가입 화면을 띄워준다.
    return render(request, 'signup.html')
"""
def signup(request):
    #HTTP Method가 POST 인 경우
    if request.method == 'POST':
        form = UserCreationMultiForm(request.POST, request.FILES) 
        #주의!! 이미지 때문에 files도 받아야함

        if form.is_valid():
            user = form['user'].save()#user저장하고
            store = form['store'].save(commit=False)
            print(store.store_image)
            store.user=user # store랑 user를 연결
            store.save() #그때 store를 저장
            auth.login(request, user)
            return redirect('home')
    
        # signup으로 GET 요청이 왔을 때, 회원가입 화면을 띄워준다.    else:
        form = UserCreationMultiForm()
    
    return render(request, 'signup.html', {'signup_form':form})


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
