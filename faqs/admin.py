"""
FAQs admin: categories and questions. Questions are shown nested in the
category for an easier workflow.
"""
from django.contrib import admin

from .models import FAQ, FAQCategory


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ('question', 'answer', 'order', 'is_published')
    show_change_link = True


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'faq_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_editable = ('order',)
    inlines = [FAQInline]

    def faq_count(self, obj):
        return obj.faqs.count()
    faq_count.short_description = 'Preguntas'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_published', 'order', 'updated_at')
    list_filter = ('is_published', 'category')
    search_fields = ('question', 'answer')
    list_editable = ('is_published', 'order')
    raw_id_fields = ('category',)
    readonly_fields = ('created_at', 'updated_at')
