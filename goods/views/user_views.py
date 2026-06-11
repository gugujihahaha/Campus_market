from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from goods.forms.profile_form import UserProfileForm
from goods.models import UserProfile


# 登录功能
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # 输入校验
        errors = []
        if not username:
            errors.append('请输入用户名')
        if not password:
            errors.append('请输入密码')
        if errors:
            return render(request, 'login.html', {'error': '；'.join(errors)})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 确保 UserProfile 存在
            UserProfile.objects.get_or_create(user=user)
            next_url = request.GET.get('next', '/goods/')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})

    return render(request, 'login.html')


# 注册功能
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # 输入校验
        errors = []
        if not username:
            errors.append('请输入用户名')
        elif len(username) < 3:
            errors.append('用户名至少需要3个字符')
        elif len(username) > 20:
            errors.append('用户名不能超过20个字符')
        elif not username.replace('_', '').replace('-', '').isalnum():
            errors.append('用户名只能包含字母、数字、下划线和连字符')

        if not password:
            errors.append('请输入密码')
        elif len(password) < 6:
            errors.append('密码至少需要6个字符')

        if errors:
            return render(request, 'register.html', {'error': '；'.join(errors)})

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': '用户名已存在'})

        # 创建用户
        try:
            user = User.objects.create_user(username=username, password=password)
        except Exception as e:
            return render(request, 'register.html',
                          {'error': f'注册失败：{str(e)}'})

        # 确保 UserProfile 在登录前创建
        UserProfile.objects.get_or_create(user=user)

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
    # 确保 UserProfile 存在
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

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