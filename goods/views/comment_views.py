import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from goods.models import Goods, Comment
from goods.services.notification_service import send_notification

MAX_COMMENT_LENGTH = 500


def build_comment_tree(comments_qs):
    """将扁平的评论列表构建为树形结构（顶层评论 + 嵌套回复）"""
    comments = []
    reply_map = {}

    for c in comments_qs:
        data = {
            "id": c.id,
            "user": c.user.username,
            "display_name": c.user.profile.display_name,
            "avatar_url": c.user.profile.avatar.url if c.user.profile.avatar else None,
            "initial": c.user.profile.display_name[:1].upper(),
            "content": c.content,
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M"),
            "parent_id": c.parent_id,
            "replies": [],
            "is_owner": False,  # will be set by caller
        }
        if c.parent_id:
            reply_map.setdefault(c.parent_id, []).append(data)
        else:
            comments.append(data)

    # 递归填充回复
    def attach_replies(comment_list):
        for item in comment_list:
            item["replies"] = reply_map.get(item["id"], [])
            attach_replies(item["replies"])

    attach_replies(comments)
    return comments


def comment_list(request, goods_id):
    """获取商品留言列表（JSON）"""
    goods = get_object_or_404(Goods, id=goods_id)
    comments_qs = goods.comments.select_related(
        "user", "user__profile", "parent"
    ).order_by("-created_at")

    comments = build_comment_tree(comments_qs)

    # 标注当前用户是否为留言作者
    for c in _flatten(comments):
        c["is_owner"] = request.user.is_authenticated and c["user"] == request.user.username

    return JsonResponse({
        "success": True,
        "comments": comments,
        "total": comments_qs.count(),
        "is_authenticated": request.user.is_authenticated,
        "current_user": request.user.username if request.user.is_authenticated else "",
        "goods_owner": goods.user.username,
    })


@login_required
@require_POST
def comment_add(request, goods_id):
    """添加留言或回复"""
    goods = get_object_or_404(Goods, id=goods_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "请求数据格式错误"}, status=400)

    content = data.get("content", "").strip()
    parent_id = data.get("parent_id")

    # 后端校验
    if not content:
        return JsonResponse({"success": False, "error": "留言内容不能为空"}, status=400)
    if len(content) > MAX_COMMENT_LENGTH:
        return JsonResponse({"success": False, "error": f"留言不能超过{MAX_COMMENT_LENGTH}字"}, status=400)

    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id, goods=goods)
        # 只允许一级回复（回复的回复就指向同一父级）
        if parent.parent_id:
            parent = parent.parent

    comment = Comment.objects.create(
        goods=goods,
        user=request.user,
        parent=parent,
        content=content,
    )

    # 通知卖家（非自己留言时）
    if request.user != goods.user:
        send_notification(
            recipient=goods.user,
            type_="new_comment",
            title=f"{request.user.profile.display_name} 给你的商品留言了",
            content=content[:100],
            link=f"/goods/detail/{goods.id}/",
            sender=request.user,
        )

    return JsonResponse({
        "success": True,
        "comment": {
            "id": comment.id,
            "user": comment.user.username,
            "display_name": comment.user.profile.display_name,
            "avatar_url": comment.user.profile.avatar.url if comment.user.profile.avatar else None,
            "initial": comment.user.profile.display_name[:1].upper(),
            "content": comment.content,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
            "parent_id": comment.parent_id,
            "is_owner": True,
        },
    })


@login_required
@require_POST
def comment_delete(request, goods_id, comment_id):
    """删除留言（仅作者或商品所有者）"""
    goods = get_object_or_404(Goods, id=goods_id)
    comment = get_object_or_404(Comment, id=comment_id, goods=goods)

    # 权限校验：留言作者 或 商品所有者
    if comment.user != request.user and goods.user != request.user:
        return JsonResponse({"success": False, "error": "无权删除此留言"}, status=403)

    comment.delete()
    return JsonResponse({"success": True})


def _flatten(comments):
    """递归平铺评论树"""
    for c in comments:
        yield c
        yield from _flatten(c.get("replies", []))
