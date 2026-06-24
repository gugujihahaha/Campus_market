from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from goods.forms.profile_form import UserProfileForm
from goods.forms.password_reset_form import PasswordResetRequestForm, PasswordResetForm
from goods.forms.campus_form import CampusVerifyForm
from goods.models import UserProfile, PasswordResetToken


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


# ==================== 找回密码 ====================

def password_reset_request(request):
    """忘记密码 —— 输入用户名和邮箱，发送重置链接"""
    if request.user.is_authenticated:
        return redirect('/goods/')

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            # 生成重置令牌
            reset_token = PasswordResetToken.generate(user)
            # 在开发环境中直接显示令牌链接
            reset_link = request.build_absolute_uri(
                f'/goods/password-reset/{reset_token.token}/'
            )
            messages.success(
                request,
                f"重置链接已生成（开发模式）：{reset_link}"
            )
            return render(request, 'password_reset_done.html', {
                'reset_link': reset_link,
                'username': username,
            })
    else:
        form = PasswordResetRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})


def password_reset_confirm(request, token):
    """验证令牌并重置密码"""
    if request.user.is_authenticated:
        return redirect('/goods/')

    reset_token = get_object_or_404(PasswordResetToken, token=token)

    if not reset_token.is_valid:
        messages.error(request, "此重置链接已失效或已使用，请重新申请")
        return redirect('/goods/password-reset/')

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = reset_token.user
            user.set_password(form.cleaned_data['password'])
            user.save()
            # 标记令牌已使用
            reset_token.is_used = True
            reset_token.save()
            messages.success(request, "密码重置成功！请使用新密码登录")
            return redirect('/goods/login/')
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset_confirm.html', {
        'form': form,
        'token': token,
    })


# ==================== 校园认证 ====================

@login_required
def campus_verify(request):
    """校园身份认证申请"""
    profile = request.user.profile

    if profile.is_verified:
        messages.info(request, "你已经通过校园认证")
        return redirect('/goods/my/')

    if request.method == 'POST':
        form = CampusVerifyForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.verification_status = 'pending'
            profile.save()
            messages.success(request, "认证申请已提交，请等待管理员审核")
            return redirect('/goods/my/')
    else:
        form = CampusVerifyForm(instance=profile)

    return render(request, 'campus_verify.html', {
        'form': form,
        'profile': profile,
    })