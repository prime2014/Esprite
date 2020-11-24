from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Products, Category, ProductGallery, Comment
from cart.models import Cart, Order
from django.views.generic.edit import FormMixin, FormView
from .forms import CommentForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from decimal import Decimal
from .forms import OrderForm
from django.contrib import messages


def authenticated(request):
    if request.user.is_authenticated:
        return True
    else:
        return False


def ranger(value):
    return range(1, value + 1)


class ProductsView(ListView):
    queryset = Products.objects.all()
    paginate_by = 9
    template_name = "product/product.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context['num'] = self.cart_item_number()
        return context

    def cart_item_number(self):
        """gets the number of items in the cart to display on the cart link"""
        if self.request.user.is_authenticated:
            products = Cart.objects.filter(user=self.request.user)
            num = products.count() if len(products) else int(0)
            return num
        else:
            num = 0
            return num

    def get_queryset(self):
        if self.request.GET.get('category') and self.request.GET.get('q'):
            cat = self.request.GET.get('category')
            product = self.request.GET.get('q')
            chosen = Category.objects.get(category__icontains=cat)
            return chosen.product_cat.filter(title__icontains=product)
        elif self.request.GET.get('q'):
            cat = self.request.GET['q']
            chosen = Category.objects.get(category__icontains=cat)
            return chosen.product_cat.all()
        elif self.request.GET.get('category'):
            cat = self.request.GET.get('category')
            chosen = Category.objects.get(category__iexact=cat)
            return chosen.product_cat.all()
        else:
            return self.queryset


class ProductItemView(FormMixin, DetailView):
    queryset = Products.objects.all()
    template_name = "product/detail.html"
    context_object_name = "product"
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        """Processes the comments written through the comment form"""
        slug, month, day, year, pk = kwargs['slug'], kwargs['month'], kwargs['day'], kwargs['year'], kwargs['pk']
        params = {'slug': slug, 'month': month,
                  'day': day, 'year': year, 'pk': pk}
        form = self.form_class(request.POST)
        if request.user.is_authenticated and form.is_valid():
            entry = form.save()
            item = Products.objects.get(slug=slug)
            entry.product = item
            entry.author = request.user
            entry.save()
            return redirect(reverse('product:detail', kwargs=params))
        elif not form.is_valid():
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('/login/?next=%s' % request.path)

    def get_object(self):
        slug = self.kwargs["slug"]
        return get_object_or_404(Products, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        context["categories"] = Category.objects.all()
        comments = Comment.objects.filter(product__slug=slug)
        gallery = ProductGallery.objects.filter(product__slug=slug)
        context['gallery'] = list(gallery)
        context['comments'] = comments
        context['form'] = CommentForm()
        context['num'] = self.cart_item_number()
        return context

    def cart_item_number(self):
        """gets the number of items in the cart to display on the cart link"""
        # if there user is authenticated
        if self.request.user.is_authenticated:
            products = Cart.objects.filter(user=self.request.user)
            num = products.count() if len(products) else int(0)  # num of items in cart
            return num
        else:
            num = 0
            return num


class CartView(ProductsView):
    queryset = Cart.objects.all()
    template_name = "product/cart.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = None
        if self.request.user.is_authenticated:
            products = Cart.objects.filter(user=self.request.user)
        else:
            products = []
        context['products'] = products
        context['num'] = self.cart_item_number()
        context['total_sum'], context['vat_tax'], context['total'] = self.get_total_amount()
        return context

    def get_total_amount(self):
        """Gets the total price of all items in the cart. The Order 
            table holds the total_amount column and the vat_tax"""
        try:
            my_order = Order.objects.get(user=self.request.user, ordered=False)
            total_sum = my_order.total_amount
            vat_tax = my_order.vat_tax
            total = Decimal(total_sum) + Decimal(vat_tax)
            return [total_sum, vat_tax, total]
        except:
            total_sum = Decimal(0)
            return [total_sum, 15, 15]


def update_cart(request, pk):
    """increases the quantity of each item in the cart on clicking the + sign"""
    prev_price = 0
    id = pk
    # queryset
    selected_item = Cart.objects.get(pk=id)
    # updating the db table
    selected_item.quantity += 1
    prev_price = selected_item.price
    selected_item.price = selected_item.item.new_price * \
        Decimal(selected_item.quantity)
    selected_item.save()
    total = Order.objects.get(user=request.user, ordered=False)
    total.total_amount += selected_item.price - prev_price
    total.save()
    messages.add_message(request, messages.INFO,
                         'Quantity has been successfully updated')
    return redirect('product:cart')


def decrease_quantity(request, quantity, pk):
    """Decreases the quantity of each individual item in the cart on clicking the (-) sign"""
    url = request.META['HTTP_REFERER']
    prev_price = 0
    if int(quantity) > 1:
        id = pk
        cart_item = Cart.objects.get(pk=id)
        cart_item.quantity -= 1
        prev_price = cart_item.price
        cart_item.price = cart_item.item.new_price * \
            Decimal(cart_item.quantity)
        cart_item.save()
        order = Order.objects.get(user=request.user, ordered=False)
        order.total_amount -= prev_price - cart_item.price
        order.save()
        messages.add_message(request, messages.INFO,
                             'Quantity has been successfully updated')
        return redirect(url)
    else:
        messages.add_message(request, messages.WARNING,
                             'Quantity cannot be zero')
        return redirect(url)


def order_products(request):
    user_order = Order.objects.get(
        Q(user__username__iexact=request.user) & Q(ordered=False))
    user_order.ordered = True
    user_order.save()
    messages.add_message(request, messages.SUCCESS,
                         "Your order has been successfully processed")
    return redirect('product:checkout')


class CheckoutView(FormView):
    """Displays items in the checkout page"""
    template_name = "product/checkout.html"
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.user.is_authenticated and form.is_valid():
            firstname, lastname, email = form.cleaned_data[
                'firstname'], form.cleaned_data['lastname'], form.cleaned_data['email']
            phone, address_1, address_2 = form.cleaned_data[
                'phone'], form.cleaned_data['address_1'], form.cleaned_data['address_2']
            zip_code, state = form.cleaned_data['zip_code'], form.cleaned_data['state']

            order = Order.objects.get(user=request.user, ordered=False)
            order.firstname, order.lastname, order.email = firstname, lastname, email
            order.phone, order.address_1, order.address_2 = phone, address_1, address_2
            order.zip_code, order.state = zip_code, state

            order.save()
            messages.add_message(request, messages.INFO,
                                 "Billing information was successfully created")
            return render(request, self.template_name, context=self.get_context_data())
        elif not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        elif not form.is_valid():
            return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = None
        context["categories"] = Category.objects.all()
        if self.request.user.is_authenticated:
            products = Cart.objects.filter(user=self.request.user)
        else:
            products = []
        context['products'] = products
        context['form'] = OrderForm()
        context['num'] = self.cart_item_number()
        context['total_sum'], context['vat_tax'], context['total'] = self.get_total_amount()
        return context

    def cart_item_number(self):
        """gets the number of items in the cart to display on the cart link"""
        # if there user is authenticated
        if self.request.user.is_authenticated:
            products = Cart.objects.filter(user=self.request.user)
            num = products.count() if len(products) else int(0)  # num of items in cart
            return num
        else:
            num = 0
            return num

    def get_total_amount(self):
        """Gets the total price of all items in the cart. The Order 
            table holds the total_amount column and the vat_tax"""
        try:
            my_order = Order.objects.get(user=self.request.user, ordered=False)
            total_sum = my_order.total_amount
            vat_tax = my_order.vat_tax
            total = Decimal(total_sum) + Decimal(vat_tax)
            return [total_sum, vat_tax, total]
        except:
            total_sum = Decimal(0)
            return [total_sum, 15, 15]
