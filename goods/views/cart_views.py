from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from goods.models import Goods, CartItem, Order
from goods.services.notification_service import send_notification


@login_required
@require_POST
def cart_add(request, goods_id):
    """添加商品到购物车"""
    goods = get_object_or_404(Goods, id=goods_id)

    # 不能添加自己的商品
    if goods.user == request.user:
        return JsonResponse({"success": False, "error": "不能添加自己的商品"}, status=400)

    # 只有"在售"商品可加入购物车
    if goods.status != Goods.Status.ON_SALE:
        return JsonResponse({"success": False, "error": "该商品当前不可加入购物车"}, status=400)

    try:
        CartItem.objects.create(user=request.user, goods=goods)
    except IntegrityError:
        return JsonResponse({"success": False, "error": "已在购物车中"})

    count = CartItem.objects.filter(user=request.user).count()

    return JsonResponse({"success": True, "count": count})


@login_required
@require_POST
def cart_remove(request, item_id):
    """从购物车移除商品"""
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    count = CartItem.objects.filter(user=request.user).count()
    return JsonResponse({"success": True, "count": count})


@login_required
def cart_list(request):
    """购物车页面"""
    items = CartItem.objects.filter(
        user=request.user
    ).select_related("goods__user__profile").prefetch_related("goods__images").order_by("-created_at")

    # 过滤已下架/已售出的商品
    valid_items = []
    invalid_items = []
    for item in items:
        if item.goods.status in [Goods.Status.ON_SALE, Goods.Status.IN_TRADE]:
            valid_items.append(item)
        else:
            invalid_items.append(item)

    total_price = sum(item.goods.price for item in valid_items)

    return render(request, 'cart.html', {
        'items': valid_items,
        'invalid_items': invalid_items,
        'total_price': total_price,
        'cart_count': len(valid_items),
    })


@login_required
@require_POST
def cart_checkout(request):
    """批量下单：将购物车中所有在售商品创建订单"""
    items = CartItem.objects.filter(
        user=request.user
    ).select_related("goods")

    orders_created = []
    errors = []

    for item in items:
        goods = item.goods
        if goods.user == request.user:
            errors.append(f"「{goods.title}」是自己的商品，已跳过")
            continue
        if goods.status != Goods.Status.ON_SALE:
            errors.append(f"「{goods.title}」当前不可购买，已跳过")
            continue

        # 创建订单
        order = Order.objects.create(
            buyer=request.user,
            seller=goods.user,
            goods=goods,
            price=goods.price,
        )
        goods.status = Goods.Status.IN_TRADE
        goods.save(update_fields=["status"])

        # 通知卖家
        send_notification(
            recipient=goods.user,
            type_="order_created",
            title="有人想买你的商品",
            content=f"{request.user.profile.display_name} 对「{goods.title}」下了订单",
            link=f"/goods/orders/",
            sender=request.user,
        )

        orders_created.append(order.order_no)
        # 从购物车移除
        item.delete()

    if orders_created:
        return JsonResponse({
            "success": True,
            "count": len(orders_created),
            "orders": orders_created,
            "errors": errors if errors else None,
        })
    else:
        return JsonResponse({
            "success": False,
            "error": "没有可下单的商品",
            "detail_errors": errors,
        }, status=400)


@login_required
def cart_count(request):
    """获取购物车商品数量"""
    count = CartItem.objects.filter(user=request.user).count()
    return JsonResponse({"count": count})
