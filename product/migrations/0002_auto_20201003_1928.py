# Generated by Django 3.1.2 on 2020-10-03 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=200)),
                ('primary', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ('category',),
            },
        ),
        migrations.AddField(
            model_name='products',
            name='cat',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='product_cat', to='product.category'),
        ),
    ]
