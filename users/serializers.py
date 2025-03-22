from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password","full_name", "phone_number"]

    def create(self, validated_data):
        full_name = validated_data.pop("full_name", "")
        phone_number = validated_data.pop("phone_number", "")
        user = User.objects.create_user(**validated_data)
        user.full_name = full_name  # ✅ Save full name
        user.phone_number = phone_number  # ✅ Save phone number
        user.is_verified = False  # New users are not verified initially
        user.save()
        return user
