from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from goods.models import Notification


@login_required
def notification_list(request):
    """获取通知列表（JSON），支持分页"""
    page = int(request.GET.get("page", 1))
    per_page = 20
    qs = Notification.objects.filter(recipient=request.user).order_by("-created_at")

    total = qs.count()
    unread = qs.filter(is_read=False).count()
    notifications = qs[(page - 1) * per_page : page * per_page]

    return JsonResponse({
        "success": True,
        "total": total,
        "unread": unread,
        "has_more": page * per_page < total,
        "notifications": [
            {
                "id": n.id,
                "type": n.type,
                "type_label": n.get_type_display(),
                "title": n.title,
                "content": n.content[:100],
                "link": n.link,
                "is_read": n.is_read,
                "created_at": n.created_at.strftime("%Y-%m-%d %H:%M"),
                "relative_time": _relative_time(n.created_at),
            }
            for n in notifications
        ],
    })


@login_required
def notification_unread_count(request):
    """未读通知数"""
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({"unread": count})


@login_required
@require_POST
def notification_read(request, notification_id):
    """标记单条已读"""
    n = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    n.is_read = True
    n.save(update_fields=["is_read"])
    return JsonResponse({"success": True})


@login_required
@require_POST
def notification_read_all(request):
    """全部标记已读"""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return JsonResponse({"success": True})


def _relative_time(dt):
    """返回相对时间字符串"""
    from django.utils import timezone
    now = timezone.now()
    diff = now - dt
    seconds = diff.total_seconds()
    if seconds < 60:
        return "刚刚"
    elif seconds < 3600:
        return f"{int(seconds // 60)}分钟前"
    elif seconds < 86400:
        return f"{int(seconds // 3600)}小时前"
    elif seconds < 259200:
        return f"{int(seconds // 86400)}天前"
    else:
        return dt.strftime("%m-%d %H:%M")
