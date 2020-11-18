from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Products
from .models import Cart, Order
from django.contrib import messages
from decimal import Decimal


def request_cart(request, slug):
    url = request.META['HTTP_REFERER']
    prev_price = 0
    if request.user.is_authenticated:
        selected_item = get_object_or_404(Products, slug=slug)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, item=selected_item, price=selected_item.new_price)
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]
            if order.orderedproduct.filter(item__slug=selected_item.slug).exists():
                cart_item.quantity += 1
                prev_price = cart_item.price
                cart_item.price = Decimal(
                    cart_item.quantity) * cart_item.item.new_price
                cart_item.save()
                order.total_amount += cart_item.price - prev_price
                order.save()
                messages.info(request, 'The cart was successfully updated')
                return redirect(url)
            else:
                order.orderedproduct.add(cart_item)
                order.total_amount += cart_item.price
                order.save()
                messages.info(request, 'The item was added in the cart')
                return redirect(url)
        else:
            my_order = Order.objects.create(
                user=request.user, ordered=False, total_amount=cart_item.price)
            my_order.orderedproduct.add(cart_item)
            messages.info(request, 'The item was added in the cart')
            return redirect(url)
    else:
        return redirect('/login/?next=%s' % request.path)


def remove_cart(request, slug):
    url = request.META['HTTP_REFERER']
    order = Order.objects.filter(user=request.user, ordered=False)

    if order.exists():
        user_order = order[0]
        if user_order.orderedproduct.filter(item__slug=slug).exists():
            user = User.objects.get(username=request.user)
            cart_item = Cart.objects.get(item__slug=slug, user=user)
            ord = user_order.orderedproduct.filter(item__slug=slug)
            my_order = user_order.orderedproduct.all()
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.price = Decimal(
                    cart_item.quantity) * cart_item.item.new_price
                cart_item.save()
                return redirect(url)
            else:
                if my_order.count() > 1:
                    user_order.orderedproduct.remove(ord[0])
                else:
                    sale = Order.objects.get(user=request.user, ordered=False)
                    sale.delete()
                cart_item.delete()
                return redirect(url)
        else:
            return redirect(url)
    else:
        return redirect(url)


def remove_cart_item(request, slug):
    url = request.META['HTTP_REFERER']
    my_order = Order.objects.filter(user=request.user, ordered=False)

    if my_order.exists():
        order = my_order[0]
        if order.orderedproduct.filter(item__slug=slug).exists():
            cart_item = Cart.objects.get(user=request.user, item__slug=slug)
            item_in_order = order.orderedproduct.filter(item__slug=slug)
            order.total_amount -= cart_item.price
            order.save()
            order.orderedproduct.remove(item_in_order[0])
            cart_item.delete()
            if not order.orderedproduct.count():
                customer_order = Order.objects.get(
                    user=request.user, ordered=False)
                customer_order.delete()
            return redirect(url)
    else:
        return redirect(url)
