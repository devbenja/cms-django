"""
Portfolio admin: Categories, Works, and WorkPhotos.
WorkPhoto is shown inline in the Work admin so the editor can manage the
gallery without leaving the work page.
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import Category, PortfolioWork, WorkPhoto


class WorkPhotoInline(admin.TabularInline):
    model = WorkPhoto
    extra = 1
    fields = ('image', 'preview', 'alt_text', 'caption', 'order')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px; max-width:120px; '
                'border-radius:4px; object-fit:cover;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = 'Vista previa'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'work_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_editable = ('order',)

    def work_count(self, obj):
        return obj.works.count()
    work_count.short_description = 'Obras'


@admin.register(PortfolioWork)
class PortfolioWorkAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'year', 'location',
        'is_published', 'is_featured', 'order', 'updated_at',
    )
    list_filter = ('is_published', 'is_featured', 'category', 'year')
    search_fields = ('title', 'client', 'location', 'description_short')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_published', 'is_featured', 'order')
    date_hierarchy = 'updated_at'
    inlines = [WorkPhotoInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'client', 'location', 'year'),
        }),
        ('Descripción', {
            'fields': ('description_short', 'body'),
        }),
        ('Portada y publicación', {
            'fields': ('cover_photo', 'is_published', 'is_featured', 'order'),
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(WorkPhoto)
class WorkPhotoAdmin(admin.ModelAdmin):
    list_display = ('work', 'preview', 'alt_text', 'order')
    list_filter = ('work__category',)
    search_fields = ('alt_text', 'caption', 'work__title')
    list_editable = ('order',)
    raw_id_fields = ('work',)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:60px; max-width:90px; '
                'border-radius:4px; object-fit:cover;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = 'Vista previa'
