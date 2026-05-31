from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Goods, UserProfile, Comment


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
