from django.urls import path
from goods.views.goods_views import delete_goods_view, goods_list, add_goods, goods_detail, my_goods, off_shelf_goods, relist_goods
from goods.views.user_views import user_login, register, user_logout, profile_edit
from goods.views.comment_views import comment_list, comment_add, comment_delete
from goods.views.favorite_views import favorite_toggle, favorite_list
from goods.views.order_views import order_create, order_confirm, order_cancel, order_complete, my_orders, order_detail
from goods.views.notification_views import notification_list, notification_unread_count, notification_read, notification_read_all

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
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('<int:goods_id>/comments/', comment_list, name='comment_list'),
    path('<int:goods_id>/comment/add/', comment_add, name='comment_add'),
    path('<int:goods_id>/comment/delete/<int:comment_id>/', comment_delete, name='comment_delete'),
    path('<int:goods_id>/favorite/', favorite_toggle, name='favorite_toggle'),
    path('favorites/', favorite_list, name='favorite_list'),
    path('orders/', my_orders, name='my_orders'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('<int:goods_id>/order/create/', order_create, name='order_create'),
    path('orders/<int:order_id>/confirm/', order_confirm, name='order_confirm'),
    path('orders/<int:order_id>/cancel/', order_cancel, name='order_cancel'),
    path('orders/<int:order_id>/complete/', order_complete, name='order_complete'),
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/unread/', notification_unread_count, name='notification_unread_count'),
    path('notifications/read/<int:notification_id>/', notification_read, name='notification_read'),
    path('notifications/read-all/', notification_read_all, name='notification_read_all'),
]