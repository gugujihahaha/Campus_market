from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from goods.forms.goods_form import GoodsForm
from goods.services.goods_service import delete_goods 
from goods.models import Goods

def goods_list(request):
    goods = Goods.objects.all()
    return render(request, 'goods_list.html', {'goods': goods})

# 商品详情页
def goods_detail(request, id):
    goods = Goods.objects.get(id=id)
    return render(request, 'goods_detail.html', {'goods': goods})

# “发布商品”视图
@login_required
def add_goods(request):
    if request.method == 'POST':
        form = GoodsForm(request.POST, request.FILES)

        if form.is_valid():
            goods = form.save(commit=False)  # 先不入库
            goods.user = request.user        # 补充用户
            goods.save()

            return redirect('/goods/')
    else:
        form = GoodsForm()

    return render(request, 'add_goods.html', {'form': form})

# “我的商品”视图
@login_required
def my_goods(request):
    goods = Goods.objects.filter(user=request.user)
    return render(request, 'my_goods.html', {'goods': goods})


# 删除商品视图
@login_required
def delete_goods_view(request, id):
    delete_goods(request.user, id)
    return redirect('/goods/my/')