from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from goods.forms.profile_form import UserProfileForm


# 登录功能
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/goods/')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})

    return render(request, 'login.html')


# 注册功能
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


# 退出登录
def user_logout(request):
    logout(request)
    return redirect('/goods/')


# 编辑个人资料
@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            # 如果用户清除了头像（勾选了清除复选框）
            if request.POST.get('avatar-clear'):
                if profile.avatar:
                    profile.avatar.delete(save=False)
                profile.avatar = None

            form.save()
            messages.success(request, "个人资料已更新！")
            return redirect('/goods/my/')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user_profile.html', {
        'form': form,
        'profile': profile,
    })