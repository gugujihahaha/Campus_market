from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from goods.models import Goods, Favorite


@login_required
@require_POST
def favorite_toggle(request, goods_id):
    """切换收藏状态：已收藏→取消，未收藏→添加"""
    goods = get_object_or_404(Goods, id=goods_id)

    try:
        fav = Favorite.objects.get(user=request.user, goods=goods)
        if fav.is_active:
            # 已收藏 → 取消（软删除）
            fav.is_active = False
            fav.save(update_fields=["is_active"])
            status = "unfavorited"
        else:
            # 曾收藏但已取消 → 重新激活
            fav.is_active = True
            fav.save(update_fields=["is_active"])
            status = "favorited"
    except Favorite.DoesNotExist:
        # 从未收藏 → 新建
        Favorite.objects.create(user=request.user, goods=goods)
        status = "favorited"

    count = goods.favorites.filter(is_active=True).count()

    return JsonResponse({"status": status, "count": count})


@login_required
def favorite_list(request):
    """我的收藏列表"""
    favorites = Favorite.objects.filter(
        user=request.user,
        is_active=True,
    ).select_related("goods__user__profile").prefetch_related("goods__images").order_by("-created_at")

    return JsonResponse({
        "success": True,
        "favorites": [
            {
                "id": f.id,
                "goods_id": f.goods.id,
                "title": f.goods.title,
                "price": f.goods.price,
                "status": f.goods.status,
                "status_label": f.goods.status_label,
                "image_url": f.goods.first_image.url if f.goods.first_image else None,
                "images_count": f.goods.images.count(),
                "view_count": f.goods.view_count,
                "created_at": f.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for f in favorites
        ],
        "count": favorites.count(),
    })
