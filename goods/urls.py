from django.urls import path
from goods.views.goods_views import (
    delete_goods_view, goods_list, add_goods, goods_detail,
    my_goods, off_shelf_goods, relist_goods, edit_goods,
)
from goods.views.user_views import (
    user_login, register, user_logout, profile_edit,
    password_reset_request, password_reset_confirm, campus_verify,
)
from goods.views.comment_views import comment_list, comment_add, comment_delete
from goods.views.favorite_views import favorite_toggle, favorite_list
from goods.views.order_views import (
    order_create, order_confirm, order_cancel, order_complete,
    my_orders, order_detail, review_create, user_reviews,
)
from goods.views.notification_views import (
    notification_list, notification_unread_count,
    notification_read, notification_read_all,
)
from goods.views.cart_views import (
    cart_add, cart_remove, cart_list, cart_checkout, cart_count,
)

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
    path('edit/<int:id>/', edit_goods, name='edit_goods'),
    path('profile/edit/', profile_edit, name='profile_edit'),

    # 找回密码
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset/<str:token>/', password_reset_confirm, name='password_reset_confirm'),

    # 校园认证
    path('campus-verify/', campus_verify, name='campus_verify'),

    # 留言
    path('<int:goods_id>/comments/', comment_list, name='comment_list'),
    path('<int:goods_id>/comment/add/', comment_add, name='comment_add'),
    path('<int:goods_id>/comment/delete/<int:comment_id>/', comment_delete, name='comment_delete'),

    # 收藏
    path('<int:goods_id>/favorite/', favorite_toggle, name='favorite_toggle'),
    path('favorites/', favorite_list, name='favorite_list'),

    # 订单
    path('orders/', my_orders, name='my_orders'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('<int:goods_id>/order/create/', order_create, name='order_create'),
    path('orders/<int:order_id>/confirm/', order_confirm, name='order_confirm'),
    path('orders/<int:order_id>/cancel/', order_cancel, name='order_cancel'),
    path('orders/<int:order_id>/complete/', order_complete, name='order_complete'),

    # 评价
    path('orders/<int:order_id>/review/', review_create, name='review_create'),
    path('user/<int:user_id>/reviews/', user_reviews, name='user_reviews'),

    # 通知
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/unread/', notification_unread_count, name='notification_unread_count'),
    path('notifications/read/<int:notification_id>/', notification_read, name='notification_read'),
    path('notifications/read-all/', notification_read_all, name='notification_read_all'),

    # 购物车
    path('cart/', cart_list, name='cart_list'),
    path('cart/add/<int:goods_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', cart_remove, name='cart_remove'),
    path('cart/checkout/', cart_checkout, name='cart_checkout'),
    path('cart/count/', cart_count, name='cart_count'),
]
