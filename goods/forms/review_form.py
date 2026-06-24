from django import forms
from goods.models import Review


class ReviewForm(forms.ModelForm):
    """订单评价表单"""

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{'⭐' * i}") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '说说你的交易体验吧（选填）',
                'class': 'w-full px-4 py-3 text-sm text-gray-900 bg-gray-50 border border-gray-200 rounded-xl',
            }),
        }
