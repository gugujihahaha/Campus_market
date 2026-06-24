from django import forms


class PasswordResetRequestForm(forms.Form):
    """忘记密码 —— 输入用户名和邮箱"""
    username = forms.CharField(
        max_length=20,
        min_length=3,
        label="用户名",
        widget=forms.TextInput(attrs={
            'placeholder': '请输入你的用户名',
            'class': 'w-full px-4 py-3 text-sm text-gray-900 bg-gray-50 border border-gray-200 rounded-xl',
        }),
    )
    email = forms.EmailField(
        label="注册邮箱",
        widget=forms.EmailInput(attrs={
            'placeholder': '请输入你绑定的邮箱地址',
            'class': 'w-full px-4 py-3 text-sm text-gray-900 bg-gray-50 border border-gray-200 rounded-xl',
        }),
    )

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username', '').strip()
        email = cleaned.get('email', '').strip()
        from django.contrib.auth.models import User
        from goods.models import UserProfile

        if username and email:
            try:
                user = User.objects.get(username=username)
                profile = user.profile
                if profile.email != email:
                    raise forms.ValidationError("用户名与邮箱不匹配，请检查后重试")
            except User.DoesNotExist:
                raise forms.ValidationError("该用户名不存在")
        return cleaned


class PasswordResetForm(forms.Form):
    """重置密码 —— 输入新密码"""
    password = forms.CharField(
        min_length=6,
        label="新密码",
        widget=forms.PasswordInput(attrs={
            'placeholder': '请输入新密码（至少6个字符）',
            'class': 'w-full px-4 py-3 text-sm text-gray-900 bg-gray-50 border border-gray-200 rounded-xl',
        }),
    )
    password_confirm = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.PasswordInput(attrs={
            'placeholder': '请再次输入新密码',
            'class': 'w-full px-4 py-3 text-sm text-gray-900 bg-gray-50 border border-gray-200 rounded-xl',
        }),
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password_confirm')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("两次输入的密码不一致")
        return cleaned
