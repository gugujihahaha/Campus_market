from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Goods(models.Model):
    title = models.CharField(max_length=100)  # 标题
    price = models.FloatField()               # 价格
    description = models.TextField()          # 描述
    created_at = models.DateTimeField(auto_now_add=True)  # 发布时间

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='goods/', null=True, blank=True)
    
    def __str__(self):
        return self.title