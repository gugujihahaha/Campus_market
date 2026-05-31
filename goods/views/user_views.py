from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User 

# 新增：登录功能
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/goods/')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})

    return render(request, 'login.html')


# 新增：注册功能
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 简单校验
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': '用户名已存在'})

        # 创建用户（密码会自动加密）
        user = User.objects.create_user(username=username, password=password)

        # 自动登录
        login(request, user)

        return redirect('/goods/')

    return render(request, 'register.html')