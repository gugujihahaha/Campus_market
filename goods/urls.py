from django.urls import path
from goods.views.goods_views import delete_goods_view, goods_list, add_goods, goods_detail, my_goods
from goods.views.user_views import user_login, register

urlpatterns = [
    path('', goods_list),
    path('login/', user_login),
    path('register/', register),
    path('add/', add_goods),
    path('detail/<int:id>/', goods_detail),
    path('my/', my_goods),
    path('delete/<int:id>/', delete_goods_view),
]