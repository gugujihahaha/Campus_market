from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ==================== Category 商品分类 ====================

class Category(models.Model):
    """商品分类模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name="分类名称")
    icon = models.CharField(
        max_length=20,
        default="📦",
        verbose_name="图标",
        help_text="可使用 Emoji 表情或图标类名",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"
        ordering = ["id"]

    def __str__(self):
        return f"{self.icon} {self.name}"

    @property
    def goods_count(self):
        """该分类下的商品数量"""
        return self.goods_set.count()


# ==================== Goods 商品 ====================

class Goods(models.Model):
    """商品模型"""

    class Status(models.IntegerChoices):
        ON_SALE = 0, "在售"
        IN_TRADE = 1, "交易中"
        SOLD = 2, "已售出"
        OFF_SHELF = 3, "已下架"

    title = models.CharField(max_length=100, verbose_name="标题")
    price = models.FloatField(verbose_name="价格")
    description = models.TextField(verbose_name="描述")
    image = models.ImageField(upload_to="goods/", null=True, blank=True, verbose_name="图片")

    # 外键 & 归属
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="分类",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="发布者")

    # 状态 & 统计
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.ON_SALE,
        verbose_name="状态",
        db_index=True,
    )
    view_count = models.PositiveIntegerField(default=0, verbose_name="浏览量")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def status_label(self):
        """获取状态的纯文字描述"""
        return self.Status(self.status).label if self.status in self.Status.values else "未知"

    def increment_view(self):
        """浏览量 +1（避免竞态，使用 F 表达式）"""
        self.view_count = models.F("view_count") + 1
        self.save(update_fields=["view_count"])
        self.refresh_from_db(fields=["view_count"])

    @property
    def first_image(self):
        """获取第一张图片（优先多图，fallback 到旧单图字段）"""
        img = self.images.first()
        if img:
            return img.image
        return self.image

    @property
    def favorite_count(self):
        """有效收藏数"""
        return self.favorites.filter(is_active=True).count()


# ==================== GoodsImage 商品多图 ====================

class GoodsImage(models.Model):
    """商品多图模型 —— 一个商品可关联多张图片"""
    goods = models.ForeignKey(
        Goods,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="商品",
    )
    image = models.ImageField(upload_to="goods/", verbose_name="图片")
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="排序")

    class Meta:
        verbose_name = "商品图片"
        verbose_name_plural = "商品图片"
        ordering = ["sort_order", "upload_time"]

    def __str__(self):
        return f"{self.goods.title} — 图片 {self.sort_order}"


# ==================== UserProfile 用户资料 ====================

class UserProfile(models.Model):
    """用户扩展资料模型"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="用户",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        verbose_name="头像",
    )
    nickname = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="昵称",
        help_text="显示在商品页面上的名称",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="手机号",
    )
    wechat = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="微信号",
    )
    contact_info = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="联系方式",
        help_text="其他联系方式（QQ 等）",
    )
    dormitory = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="所在宿舍区",
        help_text="例如：南区3栋 / 北区5号楼",
    )
    bio = models.TextField(
        max_length=200,
        blank=True,
        verbose_name="个人简介",
        help_text="简单介绍一下自己，让交易更放心（200字以内）",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self):
        return f"{self.user.username} 的资料"

    @property
    def display_name(self):
        """返回昵称或用户名"""
        return self.nickname or self.user.username


# ==================== Comment 商品留言 ====================

class Comment(models.Model):
    """商品留言模型 —— 支持嵌套回复"""
    goods = models.ForeignKey(
        Goods,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="商品",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="留言者",
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name="父评论",
    )
    content = models.TextField(verbose_name="留言内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="留言时间")

    class Meta:
        verbose_name = "商品留言"
        verbose_name_plural = "商品留言"
        ordering = ["-created_at"]

    def __str__(self):
        prefix = "回复" if self.parent_id else "评论"
        return f"{self.user.username} {prefix} → {self.goods.title}: {self.content[:30]}"

    @property
    def is_reply(self):
        return self.parent_id is not None


# ==================== Favorite 收藏 ====================

class Favorite(models.Model):
    """商品收藏模型"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="用户",
    )
    goods = models.ForeignKey(
        Goods,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="商品",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="有效",
        help_text="商品下架/删除时标记为 False，保留收藏记录",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = "收藏"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "goods"],
                name="unique_user_goods_favorite",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.goods.title}"


import random
from datetime import datetime


def generate_order_no():
    """生成唯一订单号：年月日时分秒 + 4位随机数"""
    now = datetime.now()
    rand = str(random.randint(1000, 9999))
    return now.strftime("%Y%m%d%H%M%S") + rand


# ==================== Order 订单 ====================

class Order(models.Model):
    """交易订单模型"""

    class Status(models.IntegerChoices):
        PENDING = 0, "待确认"
        IN_TRADE = 1, "交易中"
        COMPLETED = 2, "已完成"
        CANCELLED = 3, "已取消"

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buy_orders",
        verbose_name="买家",
        db_index=True,
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sell_orders",
        verbose_name="卖家",
        db_index=True,
    )
    goods = models.ForeignKey(
        "Goods",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="商品",
    )
    order_no = models.CharField(
        max_length=20,
        unique=True,
        default=generate_order_no,
        verbose_name="订单编号",
    )
    price = models.FloatField(verbose_name="成交价格")
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="状态",
        db_index=True,
    )
    cancel_reason = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="取消原因",
    )
    cancelled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cancelled_orders",
        verbose_name="取消人",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="下单时间", db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"
        ordering = ["-created_at"]

    def __str__(self):
        return f"订单 {self.order_no}: {self.buyer.username} → {self.seller.username}"

    @property
    def status_label(self):
        return self.Status(self.status).label

    @property
    def other_user(self):
        """返回当前用户的对方（在视图层传 user 不方便时用）"""
        return None  # 替代逻辑在视图中处理


# ==================== Notification 通知 ====================

class Notification(models.Model):
    """站内消息通知模型"""

    class Type(models.TextChoices):
        NEW_COMMENT = "new_comment", "新留言"
        ORDER_CREATED = "order_created", "新订单"
        ORDER_CONFIRMED = "order_confirmed", "订单已确认"
        ORDER_CANCELLED = "order_cancelled", "订单已取消"
        ORDER_COMPLETED = "order_completed", "交易完成"
        SYSTEM = "system", "系统通知"

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="接收者",
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_notifications",
        verbose_name="发送者",
    )
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        verbose_name="通知类型",
    )
    title = models.CharField(max_length=100, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    link = models.CharField(max_length=200, blank=True, verbose_name="跳转链接")
    is_read = models.BooleanField(default=False, verbose_name="已读")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="时间")

    class Meta:
        verbose_name = "通知"
        verbose_name_plural = "通知"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_type_display()}] {self.title[:30]}"


# ==================== 信号：自动创建 UserProfile ====================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """新建 User 时自动创建对应的 UserProfile"""
    if created:
        UserProfile.objects.get_or_create(user=instance)
