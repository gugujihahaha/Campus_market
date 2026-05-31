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
    contact_info = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="联系方式",
        help_text="微信 / QQ / 手机号",
    )
    dormitory = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="所在宿舍区",
        help_text="例如：南区3栋 / 北区5号楼",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self):
        return f"{self.user.username} 的资料"


# ==================== Comment 商品留言 ====================

class Comment(models.Model):
    """商品留言模型"""
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
    content = models.TextField(verbose_name="留言内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="留言时间")

    class Meta:
        verbose_name = "商品留言"
        verbose_name_plural = "商品留言"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} → {self.goods.title}: {self.content[:30]}"


# ==================== 信号：自动创建 UserProfile ====================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """新建 User 时自动创建对应的 UserProfile"""
    if created:
        UserProfile.objects.create(user=instance)
