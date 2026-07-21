"""
Testimonial admin: client quotes shown on the home page.
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        'client_name', 'client_company', 'related_work',
        'is_published', 'order', 'preview', 'created_at',
    )
    list_filter = ('is_published', 'related_work__category')
    search_fields = ('client_name', 'client_company', 'client_role', 'quote')
    list_editable = ('is_published', 'order')
    raw_id_fields = ('related_work',)
    readonly_fields = ('created_at', 'preview_large')

    fieldsets = (
        (None, {
            'fields': ('client_name', 'client_role', 'client_company', 'client_photo', 'preview_large'),
        }),
        ('Cita', {
            'fields': ('quote', 'related_work'),
        }),
        ('Publicación', {
            'fields': ('is_published', 'order'),
        }),
        ('Metadatos', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def preview(self, obj):
        if obj.client_photo:
            return format_html(
                '<img src="{}" style="width:40px; height:40px; border-radius:50%; '
                'object-fit:cover;" />',
                obj.client_photo.url,
            )
        return '—'
    preview.short_description = 'Foto'

    def preview_large(self, obj):
        if obj.client_photo:
            return format_html(
                '<img src="{}" style="max-height:200px; border-radius:6px;" />',
                obj.client_photo.url,
            )
        return '—'
    preview_large.short_description = 'Foto del cliente'
