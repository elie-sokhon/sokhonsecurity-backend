from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='media/product_images/')
    pdf_file = models.FileField(upload_to='media/product_pdfs/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hover_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    feature1 = models.TextField(blank=True, null=True)
    feature2 = models.TextField(blank=True, null=True)
    feature3 = models.TextField(blank=True, null=True)
    feature4 = models.TextField(blank=True, null=True)
    feature5 = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    category = models.CharField(max_length=255, blank=True, null=True)
    subcategory = models.CharField(max_length=255, blank=True, null=True)
    

    def __str__(self):
        return self.name
