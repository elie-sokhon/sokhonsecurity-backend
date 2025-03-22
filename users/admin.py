from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # ✅ Import the custom user model

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "full_name", "phone_number", "is_verified", "is_staff", "is_superuser")  # ✅ Show these fields in the admin panel
    search_fields = ("username", "email", "full_name", "phone_number")  # ✅ Add search functionality
    list_filter = ("is_verified", "is_staff", "is_superuser")  # ✅ Filter users easily

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("full_name", "phone_number","is_verified")}),  # ✅ Show fields in user details page
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("full_name", "phone_number","is_verified")}),  # ✅ Show fields when adding a new user
    )

    

