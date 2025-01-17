# Generated by Django 3.1.2 on 2020-10-11 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20201005_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, default='', upload_to='')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_gallery', to='product.products')),
            ],
            options={
                'verbose_name_plural': 'Product Gallery',
                'ordering': ('-date_uploaded',),
            },
        ),
    ]
