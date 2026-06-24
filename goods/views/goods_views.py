from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
import random
from goods.forms.goods_form import GoodsForm, validate_images
from goods.services.goods_service import delete_goods as delete_goods_service
from goods.models import Goods, Category, GoodsImage, Favorite, Announcement


def goods_list(request):
    """商品列表页 —— 搜索 + 分类 + 排序 + 价格 + 翻页"""
    category_id = request.GET.get("category", "")
    keyword = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "default")
    price_min = request.GET.get("price_min", "").strip()
    price_max = request.GET.get("price_max", "").strip()
    page = request.GET.get("page", "1")

    categories = Category.objects.all()

    goods = Goods.objects.filter(status__in=[0, 1]).prefetch_related("images").annotate(
        fav_count=models.Count("favorites", filter=models.Q(favorites__is_active=True))
    )

    if category_id and category_id.isdigit():
        goods = goods.filter(category_id=int(category_id))
        current_category = category_id
        current_category_name = categories.filter(id=int(category_id)).first()
        current_category_name = current_category_name.name if current_category_name else ""
    else:
        current_category = ""
        current_category_name = ""

    if keyword:
        goods = goods.filter(
            models.Q(title__icontains=keyword) | models.Q(description__icontains=keyword)
        )

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

    sort_map = {
        "default": "-created_at",
        "price_asc": "price",
        "price_desc": "-price",
        "newest": "-created_at",
        "most_viewed": "-view_count",
    }
    goods = goods.order_by(sort_map.get(sort, "-created_at"))

    # 翻页
    paginator = Paginator(goods, 12)
    try:
        page_obj = paginator.page(int(page))
    except (ValueError, EmptyPage):
        page_obj = paginator.page(1)

    announcements = Announcement.objects.filter(is_active=True).order_by("-created_at")[:3]

    context = {
        "goods": page_obj,
        "page_obj": page_obj,
        "categories": categories,
        "current_category": current_category,
        "current_category_name": current_category_name,
        "keyword": keyword,
        "sort": sort,
        "price_min": price_min,
        "price_max": price_max,
        "announcements": announcements,
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

    # 商品推荐：同分类推荐 + 随机热门
    recommended = _get_recommendations(goods, request.user)

    # 卖家评价
    seller_reviews = goods.user.received_reviews.select_related(
        "reviewer", "order"
    ).order_by("-created_at")[:5]
    seller_avg_rating = goods.user.profile.avg_rating
    seller_review_count = goods.user.profile.review_count

    # 卖家其他在售商品
    seller_other = Goods.objects.filter(
        user=goods.user, status__in=[0, 1]
    ).exclude(id=goods.id).prefetch_related("images").order_by("-created_at")[:6]

    return render(request, 'goods_detail.html', {
        'goods': goods,
        'images': images,
        'images_count': len(images),
        'is_favorited': is_favorited,
        'favorite_count': goods.favorite_count,
        'recommended': recommended,
        'seller_reviews': seller_reviews,
        'seller_avg_rating': seller_avg_rating,
        'seller_review_count': seller_review_count,
        'seller_other': seller_other,
    })


def _get_recommendations(goods, user):
    """生成推荐商品列表"""
    recommended = []
    # 1. 同分类商品
    if goods.category:
        same_cat = Goods.objects.filter(
            category=goods.category,
            status__in=[0, 1],
        ).exclude(id=goods.id).prefetch_related("images").order_by("-view_count")[:4]
        recommended.extend(same_cat)

    # 2. 随机热门补充
    remaining = 6 - len(recommended)
    if remaining > 0:
        hot = Goods.objects.filter(
            status__in=[0, 1],
        ).exclude(id=goods.id).exclude(
            id__in=[g.id for g in recommended]
        ).prefetch_related("images").order_by("-view_count")[:remaining * 3]
        hot_list = list(hot)
        random.shuffle(hot_list)
        recommended.extend(hot_list[:remaining])

    return recommended[:6]


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


# 编辑商品视图
@login_required
def edit_goods(request, id):
    goods = get_object_or_404(Goods, id=id, user=request.user)

    if request.method == 'POST':
        form = GoodsForm(request.POST, instance=goods)
        image_files = request.FILES.getlist('images')
        image_errors = validate_images(image_files)

        # 处理图片删除
        delete_image_ids = request.POST.getlist('delete_images')
        if delete_image_ids:
            for img_id in delete_image_ids:
                GoodsImage.objects.filter(id=img_id, goods=goods).delete()

        if form.is_valid() and not image_errors:
            goods = form.save()

            # 追加新图片
            for idx, img_file in enumerate(image_files):
                GoodsImage.objects.create(
                    goods=goods,
                    image=img_file,
                    sort_order=goods.images.count() + idx,
                )

            messages.success(request, "商品信息已更新！")
            return redirect('/goods/my/')
        else:
            for err in image_errors:
                messages.error(request, err)
    else:
        form = GoodsForm(instance=goods)

    categories = Category.objects.all()
    existing_images = goods.images.all()

    return render(request, 'edit_goods.html', {
        'form': form,
        'goods': goods,
        'categories': categories,
        'existing_images': existing_images,
        'existing_count': existing_images.count(),
    })