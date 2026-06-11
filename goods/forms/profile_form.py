from django import forms
from goods.models import UserProfile

ALLOWED_AVATAR_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
MAX_AVATAR_SIZE = 3 * 1024 * 1024  # 3MB


class UserProfileForm(forms.ModelForm):
    """用户资料编辑表单"""

    class Meta:
        model = UserProfile
        fields = ['avatar', 'nickname', 'phone', 'wechat', 'dormitory', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            ext = '.' + avatar.name.split('.')[-1].lower()
            if ext not in ALLOWED_AVATAR_EXTENSIONS:
                raise forms.ValidationError("头像仅支持 JPG/PNG/WebP 格式")
            if avatar.size > MAX_AVATAR_SIZE:
                raise forms.ValidationError("头像文件不能超过 3MB")
        return avatar

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and not phone.isdigit():
            raise forms.ValidationError("手机号只能包含数字")
        if phone and len(phone) != 11:
            raise forms.ValidationError("请输入11位手机号")
        return phone

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '').strip()
        if len(bio) > 200:
            raise forms.ValidationError("个人简介不能超过200字")
        return bio
