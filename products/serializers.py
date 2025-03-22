from rest_framework import serializers
from .models import Product
from django.contrib.auth import get_user_model  # ✅ Use the correct user model

User = get_user_model()  # ✅ Ensure Django uses the custom user model

class ProductSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'title', 'description', 'image', 'hover_image', 'pdf_file', 'price', 'pdf_url','feature1',
                  'feature2','feature3','feature4','feature5','featured','category','subcategory']

    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file:
            return request.build_absolute_uri(obj.pdf_file.url)
        return None


