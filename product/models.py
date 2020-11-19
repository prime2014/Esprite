from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from datetime import datetime


class Category(models.Model):
    category = models.CharField(max_length=200, default="")
    primary = models.BooleanField(default=False)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ('category',)
        verbose_name_plural = "Categories"


class Products(models.Model):
    cat = models.ManyToManyField(
        Category, related_name="product_cat", default="")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    featured = models.BooleanField(default=False)
    preview_text = models.TextField(default="")
    full_text = models.TextField(default="")
    likes = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    new_price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2)
    thumbnail = models.ImageField(default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        date_list = datetime.strftime(self.created, '%d/%m/%Y').split('/')
        day, month, year = date_list
        return reverse("product:detail", kwargs={"pk": self.pk, 'slug': self.slug, 'year': year, 'month': month, 'day': day})


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="product_gallery")
    images = models.ImageField(default="", blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

    class Meta:
        ordering = ('-date_uploaded',)
        verbose_name_plural = "Product Gallery"


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comment", null=True)
    email = models.CharField(max_length=200, null=True)
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="product_comment", null=True)
    comment = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    rating = models.DecimalField(
        default=0.0, decimal_places=1, max_digits=2, null=True)

    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ('-published',)
        verbose_name_plural = "Comments"
