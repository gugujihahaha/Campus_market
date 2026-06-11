import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import models
from goods.models import Goods, Order
from goods.services.notification_service import send_notification


@login_required
@require_POST
def order_create(request, goods_id):
    """买家创建订单：商品状态 → 交易中"""
    goods = get_object_or_404(Goods, id=goods_id)

    # 校验：不能买自己的商品
    if goods.user == request.user:
        return JsonResponse({"success": False, "error": "不能购买自己的商品"}, status=400)

    # 校验：只有"在售"状态的商品可以下单
    if goods.status != Goods.Status.ON_SALE:
        return JsonResponse({"success": False, "error": "该商品当前不可购买"}, status=400)

    # 创建订单 + 更新商品状态
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

    return JsonResponse({
        "success": True,
        "order": {
            "id": order.id,
            "order_no": order.order_no,
            "status": order.status,
            "status_label": order.status_label,
        },
    })


@login_required
@require_POST
def order_confirm(request, order_id):
    """卖家确认订单：待确认 → 交易中"""
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.seller:
        return JsonResponse({"success": False, "error": "无权操作"}, status=403)
    if order.status != Order.Status.PENDING:
        return JsonResponse({"success": False, "error": "订单状态不正确"}, status=400)

    order.status = Order.Status.IN_TRADE
    order.save(update_fields=["status"])

    # 通知买家
    send_notification(
        recipient=order.buyer,
        type_="order_confirmed",
        title="卖家已确认订单",
        content=f"「{order.goods.title}」的卖家已确认交易，快去联系吧",
        link=f"/goods/orders/",
        sender=request.user,
    )

    return JsonResponse({"success": True, "status": order.status, "status_label": order.status_label})


@login_required
@require_POST
def order_cancel(request, order_id):
    """取消订单（买/卖家均可），商品状态恢复为在售"""
    order = get_object_or_404(Order, id=order_id)

    if request.user not in [order.buyer, order.seller]:
        return JsonResponse({"success": False, "error": "无权操作"}, status=403)
    if order.status not in [Order.Status.PENDING, Order.Status.IN_TRADE]:
        return JsonResponse({"success": False, "error": "当前状态不可取消"}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = {}
    reason = data.get("reason", "").strip()

    # 交易中取消必须填写原因
    if order.status == Order.Status.IN_TRADE and not reason:
        return JsonResponse({"success": False, "error": "请填写取消原因"}, status=400)

    order.status = Order.Status.CANCELLED
    order.cancel_reason = reason
    order.cancelled_by = request.user
    order.save(update_fields=["status", "cancel_reason", "cancelled_by"])

    # 恢复商品状态
    order.goods.status = Goods.Status.ON_SALE
    order.goods.save(update_fields=["status"])

    # 通知对方
    other = order.seller if request.user == order.buyer else order.buyer
    send_notification(
        recipient=other,
        type_="order_cancelled",
        title="订单已取消",
        content=f"「{order.goods.title}」的订单已被{'买家' if request.user == order.buyer else '卖家'}取消" + (f"：{reason}" if reason else ""),
        link=f"/goods/orders/",
        sender=request.user,
    )

    return JsonResponse({"success": True, "status_label": "已取消"})


@login_required
@require_POST
def order_complete(request, order_id):
    """卖家标记完成：交易中 → 已完成，商品变为已售出"""
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.seller:
        return JsonResponse({"success": False, "error": "无权操作"}, status=403)
    if order.status != Order.Status.IN_TRADE:
        return JsonResponse({"success": False, "error": "当前状态不可完成"}, status=400)

    order.status = Order.Status.COMPLETED
    order.save(update_fields=["status"])

    # 商品标记为已售出
    order.goods.status = Goods.Status.SOLD
    order.goods.save(update_fields=["status"])

    # 通知买家
    send_notification(
        recipient=order.buyer,
        type_="order_completed",
        title="交易完成！",
        content=f"「{order.goods.title}」已标记为完成，记得确认收货",
        link=f"/goods/orders/",
        sender=request.user,
    )

    return JsonResponse({"success": True, "status_label": "已完成"})


@login_required
def my_orders(request):
    """我的订单页面"""
    status_filter = request.GET.get("status", "")
    base = Order.objects.select_related("buyer__profile", "seller__profile", "goods").prefetch_related("goods__images")

    bought = base.filter(buyer=request.user)
    sold = base.filter(seller=request.user)

    if status_filter and status_filter.isdigit():
        bought = bought.filter(status=int(status_filter))
        sold = sold.filter(status=int(status_filter))

    bought = bought.order_by("-created_at")
    sold = sold.order_by("-created_at")

    # 待确认订单数（卖家的）
    pending_count = base.filter(seller=request.user, status=Order.Status.PENDING).count()

    status_labels = dict(Order.Status.choices)

    return render(request, "my_orders.html", {
        "bought_orders": bought,
        "sold_orders": sold,
        "current_filter": status_filter,
        "status_labels": status_labels,
        "pending_count": pending_count,
    })


@login_required
def order_detail(request, order_id):
    """订单详情（JSON）"""
    order = get_object_or_404(
        Order.objects.select_related("buyer__profile", "seller__profile", "goods"),
        id=order_id,
    )

    if request.user not in [order.buyer, order.seller]:
        return JsonResponse({"success": False, "error": "无权查看"}, status=403)

    # 对方信息
    other = order.seller if request.user == order.buyer else order.buyer
    is_buyer = request.user == order.buyer

    # 联系方式（仅在交易中或完成后可见）
    show_contact = order.status in [Order.Status.IN_TRADE, Order.Status.COMPLETED]

    return JsonResponse({
        "success": True,
        "order": {
            "id": order.id,
            "order_no": order.order_no,
            "price": order.price,
            "status": order.status,
            "status_label": order.status_label,
            "cancel_reason": order.cancel_reason,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": order.updated_at.strftime("%Y-%m-%d %H:%M"),
            "is_buyer": is_buyer,
            "other_user": {
                "username": other.username,
                "display_name": other.profile.display_name,
                "avatar_url": other.profile.avatar.url if other.profile.avatar else None,
                "initial": other.profile.display_name[:1].upper(),
                "dormitory": other.profile.dormitory,
                "phone": other.profile.phone if show_contact else "",
                "wechat": other.profile.wechat if show_contact else "",
                "contact_info": other.profile.contact_info if show_contact else "",
            } if other else None,
            "goods": {
                "id": order.goods.id,
                "title": order.goods.title,
                "image_url": order.goods.first_image.url if order.goods.first_image else None,
            },
        },
    })
