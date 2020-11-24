from django import forms
from .models import Comment
from cart.models import Order


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'email', 'phone',
                  'address_1', 'address_2', 'state', 'zip_code']
