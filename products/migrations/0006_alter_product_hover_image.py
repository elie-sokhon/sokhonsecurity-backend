# Generated by Django 5.1.7 on 2025-03-22 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_image_alter_product_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='hover_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/product_images/'),
        ),
    ]
