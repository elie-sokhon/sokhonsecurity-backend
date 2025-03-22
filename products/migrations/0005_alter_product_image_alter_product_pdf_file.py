# Generated by Django 5.1.7 on 2025-03-22 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_category_product_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='media/product_images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pdf_file',
            field=models.FileField(upload_to='media/product_pdfs/'),
        ),
    ]
