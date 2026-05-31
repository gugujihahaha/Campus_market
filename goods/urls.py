from django.urls import path
from goods.views.goods_views import delete_goods_view, goods_list, add_goods, goods_detail, my_goods, off_shelf_goods, relist_goods
from goods.views.user_views import user_login, register, user_logout

urlpatterns = [
    path('', goods_list, name='goods_list'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('add/', add_goods, name='add_goods'),
    path('detail/<int:id>/', goods_detail, name='goods_detail'),
    path('my/', my_goods, name='my_goods'),
    path('delete/<int:id>/', delete_goods_view, name='delete_goods'),
    path('off_shelf/<int:id>/', off_shelf_goods, name='off_shelf_goods'),
    path('relist/<int:id>/', relist_goods, name='relist_goods'),
]