from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages
from goods.forms.goods_form import GoodsForm
from goods.services.goods_service import delete_goods
from goods.models import Goods, Category


def goods_list(request):
    """商品列表页 —— 支持搜索关键词 + 分类筛选"""
    category_id = request.GET.get("category", "")
    keyword = request.GET.get("q", "").strip()
    categories = Category.objects.all()

    # 基础查询：仅展示在售 / 交易中
    goods = Goods.objects.filter(status__in=[0, 1])

    # 分类筛选
    if category_id and category_id.isdigit():
        goods = goods.filter(category_id=int(category_id))
        current_category = category_id
        current_category_name = categories.filter(id=int(category_id)).first()
        current_category_name = current_category_name.name if current_category_name else ""
    else:
        current_category = ""
        current_category_name = ""

    # 关键词搜索（标题或描述模糊匹配）
    if keyword:
        goods = goods.filter(
            models.Q(title__icontains=keyword) | models.Q(description__icontains=keyword)
        )

    goods = goods.order_by("-created_at")

    context = {
        "goods": goods,
        "categories": categories,
        "current_category": current_category,
        "current_category_name": current_category_name,
        "keyword": keyword,
    }
    return render(request, "goods_list.html", context)

# 商品详情页
def goods_detail(request, id):
    goods = get_object_or_404(Goods, id=id)
    goods.increment_view()
    return render(request, 'goods_detail.html', {'goods': goods})


# "发布商品"视图
@login_required
def add_goods(request):
    if request.method == 'POST':
        form = GoodsForm(request.POST, request.FILES)

        if form.is_valid():
            goods = form.save(commit=False)
            goods.user = request.user
            goods.save()
            return redirect('/goods/')
    else:
        form = GoodsForm()

    # 传入分类列表供表单下拉使用
    categories = Category.objects.all()
    return render(request, 'add_goods.html', {
        'form': form,
        'categories': categories,
    })

# "我的商品"视图
@login_required
def my_goods(request):
    goods = Goods.objects.filter(user=request.user).order_by("-created_at")
    # 统计数据
    on_sale_count = goods.filter(status=Goods.Status.ON_SALE).count()
    sold_count = goods.filter(status=Goods.Status.SOLD).count()
    in_trade_count = goods.filter(status=Goods.Status.IN_TRADE).count()
    off_shelf_count = goods.filter(status=Goods.Status.OFF_SHELF).count()

    return render(request, 'my_goods.html', {
        'goods': goods,
        'on_sale_count': on_sale_count,
        'sold_count': sold_count,
        'in_trade_count': in_trade_count,
        'off_shelf_count': off_shelf_count,
        'total_count': goods.count(),
    })


# 删除商品视图
@login_required
def delete_goods_view(request, id):
    delete_goods(request.user, id)
    return redirect('/goods/my/')


# 下架商品视图
@login_required
def off_shelf_goods(request, id):
    goods = get_object_or_404(Goods, id=id, user=request.user)
    if goods.status != Goods.Status.OFF_SHELF:
        goods.status = Goods.Status.OFF_SHELF
        goods.save(update_fields=["status"])
    return redirect('/goods/my/')


# 重新上架商品视图
@login_required
def relist_goods(request, id):
    goods = get_object_or_404(Goods, id=id, user=request.user)
    if goods.status == Goods.Status.OFF_SHELF:
        goods.status = Goods.Status.ON_SALE
        goods.save(update_fields=["status"])
    return redirect('/goods/my/')