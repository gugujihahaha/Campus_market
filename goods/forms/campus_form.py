from django import forms
from goods.models import UserProfile


class CampusVerifyForm(forms.ModelForm):
    """校园认证表单"""

    class Meta:
        model = UserProfile
        fields = ['student_id', 'school_name']
        widgets = {
            'student_id': forms.TextInput(attrs={
                'placeholder': '请输入你的学号',
                'class': 'w-full px-4 py-3 text-sm text-gray-900 bg-gray-50 border border-gray-200 rounded-xl',
            }),
            'school_name': forms.TextInput(attrs={
                'placeholder': '请输入你的学校全称',
                'class': 'w-full px-4 py-3 text-sm text-gray-900 bg-gray-50 border border-gray-200 rounded-xl',
            }),
        }

    def clean_student_id(self):
        sid = self.cleaned_data.get('student_id', '').strip()
        if not sid:
            raise forms.ValidationError("请填写学号")
        if len(sid) < 5 or len(sid) > 30:
            raise forms.ValidationError("学号格式不正确")
        return sid

    def clean_school_name(self):
        name = self.cleaned_data.get('school_name', '').strip()
        if not name:
            raise forms.ValidationError("请填写学校名称")
        if len(name) < 2 or len(name) > 100:
            raise forms.ValidationError("学校名称格式不正确")
        return name
