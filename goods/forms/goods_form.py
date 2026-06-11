import os
from django import forms
from goods.models import Goods

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGE_COUNT = 9


class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ['title', 'price', 'description', 'category']
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


def validate_images(image_files):
    """验证上传的图片列表，返回 (valid_files, errors)"""
    errors = []

    if len(image_files) > MAX_IMAGE_COUNT:
        errors.append(f"最多上传 {MAX_IMAGE_COUNT} 张图片，当前选择了 {len(image_files)} 张")

    for i, img in enumerate(image_files):
        # 格式校验
        ext = os.path.splitext(img.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            errors.append(f"图片 {img.name} 格式不支持，仅允许 JPG/PNG/WebP")
        # 大小校验
        if img.size > MAX_FILE_SIZE:
            errors.append(f"图片 {img.name} 超过 5MB 限制（当前 {img.size / 1024 / 1024:.1f}MB）")

    return errors