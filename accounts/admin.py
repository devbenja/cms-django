"""
Custom User admin: shows the role field, filters by role, allows search by name/email.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # Add 'role' to the fieldsets without disturbing the rest of the standard UserAdmin
    fieldsets = UserAdmin.fieldsets + (
        ('Rol del CMS', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol del CMS', {'fields': ('role', 'email', 'first_name', 'last_name')}),
    )
