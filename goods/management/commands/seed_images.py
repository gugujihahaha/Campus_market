"""
管理命令：将 picture/ 文件夹下的正确图片匹配到对应商品
用法：python manage.py seed_images
"""
import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from goods.models import Goods, GoodsImage

PICTURE_DIR = os.path.join(settings.BASE_DIR, "picture")

# 图片文件名 → 商品标题关键词（用于匹配）
IMAGE_PRODUCT_MAP = [
    ("三只松鼠坚果礼.png",     "三只松鼠"),
    ("莲蓬.png",               "多肉"),
    ("传输器.png",             "Type-C扩展坞"),
    ("充电头.png",             "充电器"),
    ("活页本.png",             "活页本"),
    ("百乐笔.png",             "百乐"),
    ("手环.png",               "小米手环"),
    ("keep瑜伽垫.png",         "瑜伽垫"),
    ("羽毛球拍.png",           "羽毛球拍"),
    ("ubl小音箱.png",          "JBL"),
    ("吉他.png",               "YAMAHA"),
    ("初音未来手办.png",       "初音未来"),
    ("游戏手柄.png",           "PS5"),
    ("游戏机.png",             "Switch"),
    ("抽屉.png",               "收纳抽屉"),
    ("床上桌.jpg",             "床上桌"),
    ("香薰.png",               "香薰"),
    ("煮锅.png",               "电煮锅"),
    ("书包.png",               "双肩包"),
    ("耐克.png",               "Nike"),
    ("C++教材.png",            "C++"),
    ("考研英语.png",           "考研"),
    ("深入理解计算机系统.png", "深入理解计算机"),
    ("算法导论.png",           "算法导论"),
    ("显示器.jpg",             "4K显示器"),
    ("鼠标.png",               "罗技"),
    ("电脑.png",               "ThinkPad"),
    ("iPad.png",               "iPad"),
    ("蓝牙耳机.png",           "AirPods"),
    ("小米手机.png",           "小米14"),
    ("华为手机.png",           "华为"),
    ("苹果手机.png",           "iPhone"),
]


class Command(BaseCommand):
    help = "用 picture/ 下正确图片替换商品数据库中的随机测试图片"

    def handle(self, *args, **options):
        # 1. 删除所有旧的 GoodsImage 记录（会同时删除物理文件）
        old_count = GoodsImage.objects.count()
        GoodsImage.objects.all().delete()
        self.stdout.write(f"[1/3] 删除旧图片记录 {old_count} 条")

        # 2. 清空旧单图字段
        goods_with_old_img = Goods.objects.exclude(image="").count()
        Goods.objects.exclude(image="").update(image=None)
        self.stdout.write(f"[2/3] 清理旧单图字段 {goods_with_old_img} 条")

        # 3. 匹配并创建新图片
        matched = 0
        unmatched_files = []
        unmatched_goods = []

        for filename, keyword in IMAGE_PRODUCT_MAP:
            filepath = os.path.join(PICTURE_DIR, filename)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f"  文件不存在: {filepath}"))
                unmatched_files.append(filename)
                continue

            # 按关键词匹配商品
            goods = Goods.objects.filter(title__icontains=keyword).first()
            if not goods:
                self.stdout.write(self.style.WARNING(f"  未找到匹配商品: {filename} (关键词: {keyword})"))
                unmatched_files.append(filename)
                continue

            # 创建 GoodsImage 记录
            with open(filepath, "rb") as f:
                django_file = File(f, name=filename)
                GoodsImage.objects.create(
                    goods=goods,
                    image=django_file,
                    sort_order=0,
                )
            matched += 1
            self.stdout.write(f"  ✓ {filename} → [{goods.category.name}] {goods.title}")

        # 4. 报告结果
        self.stdout.write(self.style.SUCCESS(
            f"\n[3/3] 完成！匹配成功 {matched} 件，"
            f"总商品 {Goods.objects.count()} 件"
        ))

        # 5. 找出没有图片的商品
        all_goods_with_img = set(
            GoodsImage.objects.values_list("goods_id", flat=True)
        )
        for g in Goods.objects.all():
            if g.id not in all_goods_with_img:
                unmatched_goods.append(g.title)

        if unmatched_goods:
            self.stdout.write(self.style.WARNING(
                f"\n以下 {len(unmatched_goods)} 件商品尚无图片："
            ))
            for t in unmatched_goods:
                self.stdout.write(f"  - {t}")

        if unmatched_files:
            self.stdout.write(self.style.WARNING(
                f"\n以下 {len(unmatched_files)} 张图片未匹配："
            ))
            for f in unmatched_files:
                self.stdout.write(f"  - {f}")
