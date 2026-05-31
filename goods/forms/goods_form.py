from django import forms
from goods.models import Goods


class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ['title', 'price', 'description', 'image', 'category']
        widgets = {
            'category': forms.Select(),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("价格不能为负数")
        if price is not None and price > 99999999:
            raise forms.ValidationError("价格超出合理范围")
        return price

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 2:
            raise forms.ValidationError("标题至少需要 2 个字符")
        return title