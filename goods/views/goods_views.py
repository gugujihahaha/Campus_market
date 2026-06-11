from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages
from goods.forms.goods_form import GoodsForm, validate_images
from goods.services.goods_service import delete_goods as delete_goods_service
from goods.models import Goods, Category, GoodsImage, Favorite


def goods_list(request):
    """商品列表页 —— 支持搜索关键词 + 分类筛选 + 排序 + 价格区间"""
    category_id = request.GET.get("category", "")
    keyword = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "default")
    price_min = request.GET.get("price_min", "").strip()
    price_max = request.GET.get("price_max", "").strip()

    categories = Category.objects.all()

    # 基础查询：仅展示在售 / 交易中，预加载多图 + 收藏计数
    goods = Goods.objects.filter(status__in=[0, 1]).prefetch_related("images").annotate(
        fav_count=models.Count("favorites", filter=models.Q(favorites__is_active=True))
    )

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

    # 价格区间筛选
    if price_min:
        try:
            goods = goods.filter(price__gte=float(price_min))
        except ValueError:
            pass
    if price_max:
        try:
            goods = goods.filter(price__lte=float(price_max))
        except ValueError:
            pass

    # 排序
    sort_map = {
        "default": "-created_at",
        "price_asc": "price",
        "price_desc": "-price",
        "newest": "-created_at",
        "most_viewed": "-view_count",
    }
    order_by = sort_map.get(sort, "-created_at")
    goods = goods.order_by(order_by)

    # 生成排序标签
    sort_labels = {
        "default": "默认排序",
        "price_asc": "价格从低到高",
        "price_desc": "价格从高到低",
        "newest": "最新发布",
        "most_viewed": "最多浏览",
    }

    # 热门搜索标签
    hot_tags = ["教材", "手机", "耳机", "自行车", "台灯", "考研", "iPad", "相机"]

    context = {
        "goods": goods,
        "categories": categories,
        "current_category": current_category,
        "current_category_name": current_category_name,
        "keyword": keyword,
        "sort": sort,
        "sort_labels": sort_labels,
        "price_min": price_min,
        "price_max": price_max,
        "hot_tags": hot_tags,
    }
    return render(request, "goods_list.html", context)

# 商品详情页
def goods_detail(request, id):
    goods = get_object_or_404(Goods, id=id)
    goods.increment_view()
    images = goods.images.all()

    # 当前用户是否已收藏
    is_favorited = False
    if request.user.is_authenticated:
        from goods.models import Favorite
        is_favorited = Favorite.objects.filter(
            user=request.user, goods=goods, is_active=True
        ).exists()

    return render(request, 'goods_detail.html', {
        'goods': goods,
        'images': images,
        'images_count': len(images),
        'is_favorited': is_favorited,
        'favorite_count': goods.favorite_count,
    })


# "发布商品"视图
@login_required
def add_goods(request):
    if request.method == 'POST':
        form = GoodsForm(request.POST)

        # 获取上传的图片列表
        image_files = request.FILES.getlist('images')

        # 后端图片校验
        image_errors = validate_images(image_files)

        if form.is_valid() and not image_errors:
            goods = form.save(commit=False)
            goods.user = request.user
            goods.save()

            # 批量保存多张图片
            for idx, img_file in enumerate(image_files):
                GoodsImage.objects.create(
                    goods=goods,
                    image=img_file,
                    sort_order=idx,
                )

            messages.success(request, "商品发布成功！")
            return redirect('/goods/')
        else:
            # 将图片校验错误添加到表单错误中展示
            for err in image_errors:
                messages.error(request, err)
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
    from goods.models import Order
    goods = Goods.objects.filter(user=request.user).prefetch_related("images").order_by("-created_at")
    # 统计数据
    on_sale_count = goods.filter(status=Goods.Status.ON_SALE).count()
    sold_count = goods.filter(status=Goods.Status.SOLD).count()
    in_trade_count = goods.filter(status=Goods.Status.IN_TRADE).count()
    off_shelf_count = goods.filter(status=Goods.Status.OFF_SHELF).count()

    # 待确认订单数
    pending_order_count = Order.objects.filter(seller=request.user, status=Order.Status.PENDING).count()

    return render(request, 'my_goods.html', {
        'goods': goods,
        'on_sale_count': on_sale_count,
        'sold_count': sold_count,
        'in_trade_count': in_trade_count,
        'off_shelf_count': off_shelf_count,
        'total_count': goods.count(),
        'pending_order_count': pending_order_count,
    })


# 删除商品视图
@login_required
def delete_goods_view(request, id):
    delete_goods_service(request.user, id)
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