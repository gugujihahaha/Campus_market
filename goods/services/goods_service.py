from goods.models import Goods


def create_goods(user, data):
    """创建商品（不含图片）"""
    title = data.get('title')
    price = float(data.get('price'))
    description = data.get('description')

    if price < 0:
        raise Exception("价格不能为负")

    return Goods.objects.create(
        title=title,
        price=price,
        description=description,
        user=user,
    )


def delete_goods(user, goods_id):
    """删除商品，并级联删除所有关联图片的物理文件"""
    goods = Goods.objects.get(id=goods_id)

    if goods.user != user:
        raise Exception("无权限删除")

    # 删除旧的单图字段物理文件（如果存在）
    if goods.image:
        goods.image.delete(save=False)

    # 删除所有多图表记录中的物理文件
    for img in goods.images.all():
        img.image.delete(save=False)

    # 删除数据库记录（CASCADE 自动清理 GoodsImage 行）
    goods.delete()

