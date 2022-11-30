from django.urls import path, include
from .views import *

urlpatterns = [
    # Cart App URLs
    path("cart/view", cart_single_view, name="cart_single_view"),
    path("cart/multi/view", cart_multi_view, name="cart_multi_view"),
    path("cart/add/<int:id>", cart_single_add, name="cart_single_add"),
    path("cart/add/<int:cart_id>/<int:id>", cart_multi_add, name="cart_multi_add"),
    path("cart/clear", cart_single_clear, name="cart_single_clear"),
    path("cart/multi/clear", cart_multi_clear, name="cart_multi_clear"),
    path("cart/add/to/<int:id>", cart_single_add_to, name="cart_single_add_to"),
    path("cart/add/to/<int:cart_id>/<int:id>", cart_multi_add_to, name="cart_multi_add_to"),
    path("cart/sub/to/<int:id>", cart_single_sub_to, name="cart_single_sub_to"),
    path("cart/sub/to/<int:cart_id>/<int:id>", cart_multi_sub_to, name="cart_multi_sub_to"),
    path("cart/del/<int:id>", cart_single_del, name="cart_single_del"),
    path("cart/multi/del/<int:cart_id>/<int:id>", cart_multi_del, name="cart_multi_del"),
]
