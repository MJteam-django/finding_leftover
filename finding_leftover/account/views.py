from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

from .forms import UserCreationMultiForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

from post.models import Store

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
            store_image = request.POST.get("store_image","")
            store = Store(user=user, store_name=store_name, store_address=store_address, store_memo=store_memo, store_image=store_image)
            store.save()
            # 로그인 한다
            auth.login(request, user)
            return redirect('post-list')
    # signup으로 GET 요청이 왔을 때, 회원가입 화면을 띄워준다.
    return render(request, 'signup.html')
    
'''
# 회원가입을 위한 function입니다. 
def signup(request):
    if request.method == "POST":
        form = UserCreationMultiForm(request.POST)
        # form이 유효한지 확인한 후에 create_user로 new_user생성(이 부분에서 username을 찾을 수 없다고 에러 발생합니다)
        username = request.POST['username']
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            auth_login(request, new_user)
            return redirect('post-list')
        else: # 유효하지 않으면 이미 존재하는 사용자 메세지 반환
            return HttpResponse('이미 존재하는 사용자입니다.')
    else: # get요청 들어오면 signup.html 띄워주기
        form = UserCreationMultiForm()
        return render(request, 'signup.html', {'form':form})
'''
def login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
        return redirect('post-list')
    
    else:
        login_form = AuthenticationForm()
    
    return render(request, 'login.html', {'login_form' : login_form})



# 로그인 완
'''
def login(request):
    # login으로 POST 요청이 들어왔을 때, 로그인 절차를 밟는다.
    if request.method == 'POST':
        # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
        username = request.POST['username']
        password = request.POST['password']

        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = auth.authenticate(request, username=username, password=password)
        
        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            return redirect('post-list')
        # 존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            return render(request, 'login.html', {'error' : 'username or password is incorrect.'})
    # login으로 GET 요청이 들어왔을때, 로그인 화면을 띄워준다.
    else:
        return render(request, 'login.html')
'''
# 로그 아웃
def logout(request):
    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == 'POST':
        auth.logout(request)
        return redirect('post-list')

    # logout으로 GET 요청이 들어왔을 때, 로그인 화면을 띄워준다.
    return render(request, 'logout.html')
