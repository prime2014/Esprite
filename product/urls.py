from django.conf.urls import url
from .views import ProductsView, ProductItemView, CartView, RequestOrder, update_cart, CheckoutView, decrease_quantity
from cart.views import request_cart, remove_cart, remove_cart_item


app_name = "product"

urlpatterns = [
    url(r'^$', ProductsView.as_view(), name="list"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)/(?P<pk>[0-9]+)/$',
        ProductItemView.as_view(), name="detail"),
    url(r'^delete-cart-item/(?P<slug>[\w-]+)/$',
        remove_cart_item, name="delete"),
    url(r'^add-cart/(?P<slug>[\w-]+)/$',
        request_cart, name="add_cart"),
    url(r'^remove-cart/(?P<slug>[\w-]+)/$', remove_cart, name="remove_cart"),
    url(r'^checkout/$', CheckoutView.as_view(), name="checkout"),
    url(r'^cart/$', CartView.as_view(), name="cart"),
    url(r'^update-cart/(?P<pk>[0-9]+)/$',
        update_cart, name="update"),
    url(r'^decrease-quantity/(?P<quantity>[0-9]+)/(?P<pk>[0-9]+)/$',
        decrease_quantity, name="decrease"),
    url(r'^order/$', RequestOrder.as_view(), name="order")
]
