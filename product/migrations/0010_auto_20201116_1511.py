# Generated by Django 3.1.2 on 2020-11-16 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_comment_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='cat',
        ),
        migrations.AddField(
            model_name='products',
            name='cat',
            field=models.ManyToManyField(default='', related_name='product_cat', to='product.Category'),
        ),
    ]
