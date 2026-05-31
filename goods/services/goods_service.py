from goods.models import Goods

def create_goods(user, data, files=None):
    title = data.get('title')
    price = float(data.get('price'))
    description = data.get('description')

    user = user
    image = files.get('image') if files else None

    if price < 0:
        raise Exception("价格不能为负")

    return Goods.objects.create(
        title=title,
        price=price,
        description=description,
        user=user,
        image=image
    )


# 删除商品
def delete_goods(user, goods_id):
    goods = Goods.objects.get(id=goods_id)

    # 安全校验
    if goods.user != user:
        raise Exception("无权限删除")

    goods.delete()

