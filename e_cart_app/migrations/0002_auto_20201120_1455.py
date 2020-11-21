# Generated by Django 3.1.3 on 2020-11-20 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('e_cart_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product/images'),
        ),
        migrations.CreateModel(
            name='Product_images',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_image', models.FileField(max_length=2555, upload_to='product/images')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_cart_app.product')),
            ],
        ),
    ]