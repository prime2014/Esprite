from django.contrib import admin
from .models import Products, Category, Comment, ProductGallery


class GalleryModel(admin.TabularInline):
    model = ProductGallery
    fields = ['images']


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'likes', 'stock',
                    'old_price', 'new_price', 'rating', 'created')
    list_filter = ('created', 'cat', 'new_price')
    date_hierarchy = 'created'
    filter_horizontal = ('cat',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryModel]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'primary')
    list_filter = ('category',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'email', 'product', 'published')
    list_filter = ('published',)
    date_hierarchy = 'published'
