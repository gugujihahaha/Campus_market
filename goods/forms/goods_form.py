from django import forms
from goods.models import Goods

class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ['title', 'price', 'description', 'image']

    # 自定义校验
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("价格不能为负")
        return price