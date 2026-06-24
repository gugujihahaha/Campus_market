from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Goods, GoodsImage, UserProfile, Comment,
    Favorite, Order, Notification, Review, CartItem,
    Announcement, PasswordResetToken,
)


# ==================== Category Admin ====================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "icon", "name", "goods_count", "created_at")
    search_fields = ("name",)
    ordering = ("id",)

    def goods_count(self, obj):
        count = obj.goods_count
        return format_html(
            '<span style="font-weight:600;color:#2563eb;">{}</span>', count
        )

    goods_count.short_description = "商品数量"


# ==================== Goods Admin ====================

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price_tag",
        "category",
        "user",
        "status_badge",
        "view_count",
        "created_at",
    )
    list_filter = (
        "status",
        "category",
        "created_at",
    )
    search_fields = ("title", "description", "user__username")
    list_select_related = ("category", "user")
    date_hierarchy = "created_at"
    readonly_fields = ("view_count", "created_at", "updated_at")

    # 按状态分组折叠
    fieldsets = (
        ("基本信息", {
            "fields": ("title", "price", "description", "image", "category"),
        }),
        ("归属与状态", {
            "fields": ("user", "status", "view_count"),
        }),
        ("时间信息", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    def price_tag(self, obj):
        return format_html(
            '<span style="color:#dc2626;font-weight:600;">¥{:.2f}</span>', obj.price
        )

    price_tag.short_description = "价格"
    price_tag.admin_order_field = "price"

    def status_badge(self, obj):
        status_map = {
            0: ("#10b981", "在售"),
            1: ("#f59e0b", "交易中"),
            2: ("#6b7280", "已售出"),
            3: ("#ef4444", "已下架"),
        }
        color, text = status_map.get(obj.status, ("#6b7280", "未知"))
        return format_html(
            '<span style="display:inline-block;padding:2px 10px;'
            'border-radius:999px;background:{};color:#fff;'
            'font-size:12px;font-weight:500;">{}</span>',
            color,
            text,
        )

    status_badge.short_description = "状态"
    status_badge.admin_order_field = "status"


# ==================== UserProfile Admin ====================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "avatar_preview", "user", "contact_info", "dormitory", "created_at")
    search_fields = ("user__username", "contact_info", "dormitory")
    list_select_related = ("user",)
    readonly_fields = ("created_at",)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width:36px;height:36px;'
                'border-radius:50%;object-fit:cover;" />',
                obj.avatar.url,
            )
        return format_html(
            '<span style="display:inline-block;width:36px;height:36px;'
            'border-radius:50%;background:#e5e7eb;text-align:center;'
            'line-height:36px;color:#9ca3af;font-size:14px;">?</span>'
        )

    avatar_preview.short_description = "头像"


# ==================== Comment Admin ====================

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "goods_link", "user", "content_brief", "created_at")
    search_fields = ("content", "user__username", "goods__title")
    list_filter = ("created_at",)
    list_select_related = ("goods", "user")
    date_hierarchy = "created_at"

    def goods_link(self, obj):
        from django.urls import reverse
        url = reverse("admin:goods_goods_change", args=[obj.goods.pk])
        return format_html('<a href="{}" style="color:#2563eb;">{}</a>', url, obj.goods.title)

    goods_link.short_description = "商品"
    goods_link.admin_order_field = "goods__title"

    def content_brief(self, obj):
        if len(obj.content) > 40:
            return obj.content[:40] + "…"
        return obj.content

    content_brief.short_description = "留言内容"


# ==================== GoodsImage Admin ====================

@admin.register(GoodsImage)
class GoodsImageAdmin(admin.ModelAdmin):
    list_display = ("id", "goods", "image_preview", "sort_order", "upload_time")
    list_filter = ("upload_time",)
    search_fields = ("goods__title",)
    list_select_related = ("goods",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:36px;border-radius:4px;object-fit:cover;" />',
                obj.image.url,
            )
        return "—"

    image_preview.short_description = "图片"


# ==================== Favorite Admin ====================

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "goods", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("user__username", "goods__title")
    list_select_related = ("user", "goods")


# ==================== Order Admin ====================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order_no", "goods", "buyer", "seller", "price_tag", "status_badge_o", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("order_no", "buyer__username", "seller__username", "goods__title")
    list_select_related = ("buyer", "seller", "goods")
    date_hierarchy = "created_at"
    readonly_fields = ("order_no", "created_at", "updated_at")

    def price_tag(self, obj):
        return format_html('<span style="color:#dc2626;font-weight:600;">¥{:.2f}</span>', obj.price)
    price_tag.short_description = "价格"
    price_tag.admin_order_field = "price"

    def status_badge_o(self, obj):
        status_map = {
            0: ("#f59e0b", "待确认"),
            1: ("#3b82f6", "交易中"),
            2: ("#10b981", "已完成"),
            3: ("#6b7280", "已取消"),
        }
        color, text = status_map.get(obj.status, ("#6b7280", "未知"))
        return format_html(
            '<span style="display:inline-block;padding:2px 10px;border-radius:999px;background:{};color:#fff;font-size:12px;font-weight:500;">{}</span>',
            color, text,
        )
    status_badge_o.short_description = "状态"
    status_badge_o.admin_order_field = "status"


# ==================== Notification Admin ====================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "title", "recipient", "sender", "is_read", "created_at")
    list_filter = ("type", "is_read", "created_at")
    search_fields = ("title", "content", "recipient__username")
    list_select_related = ("recipient", "sender")
    date_hierarchy = "created_at"


# ==================== Review Admin ====================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "order_link", "reviewer", "reviewee", "rating_stars", "comment_brief", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("reviewer__username", "reviewee__username", "comment")
    list_select_related = ("reviewer", "reviewee", "order")

    def order_link(self, obj):
        url = f"/admin/goods/order/{obj.order.pk}/change/"
        return format_html('<a href="{}" style="color:#2563eb;">#{}</a>', url, obj.order.order_no)
    order_link.short_description = "订单"

    def rating_stars(self, obj):
        return "⭐" * obj.rating
    rating_stars.short_description = "评分"

    def comment_brief(self, obj):
        if len(obj.comment) > 30:
            return obj.comment[:30] + "…"
        return obj.comment
    comment_brief.short_description = "评价内容"


# ==================== CartItem Admin ====================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "goods", "created_at")
    search_fields = ("user__username", "goods__title")
    list_select_related = ("user", "goods")
    date_hierarchy = "created_at"


# ==================== Announcement Admin ====================

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "created_by", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "content")
    list_select_related = ("created_by",)
    date_hierarchy = "created_at"

    fieldsets = (
        ("公告内容", {
            "fields": ("title", "content"),
        }),
        ("发布设置", {
            "fields": ("is_active", "created_by"),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# ==================== PasswordResetToken Admin ====================

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "token_brief", "is_used", "expires_at", "created_at")
    list_filter = ("is_used", "created_at")
    search_fields = ("user__username", "token")
    readonly_fields = ("token", "created_at")

    def token_brief(self, obj):
        return obj.token[:16] + "…"
    token_brief.short_description = "令牌"
