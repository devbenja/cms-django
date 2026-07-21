"""
Page admin: corporate pages with editorial workflow (draft/published/archived).
Status, in-menu, and date columns are the most useful for the editor.
"""
from django.contrib import admin

from .models import Page, PageStatus


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'is_in_menu', 'menu_order', 'author', 'published_at', 'updated_at')
    list_filter = ('status', 'is_in_menu', 'created_at', 'updated_at')
    search_fields = ('title', 'slug', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    date_hierarchy = 'updated_at'
    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status'),
        }),
        ('Contenido', {
            'fields': ('body',),
            'description': 'Lista de bloques (heading, paragraph, image, cta, quote, list, gallery, video_embed). En Fase 4 se reemplaza por un editor visual.',
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'og_image'),
            'classes': ('collapse',),
        }),
        ('Navegación', {
            'fields': ('is_in_menu', 'menu_order'),
        }),
        ('Metadatos', {
            'fields': ('author', 'published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Creating a new page
            obj.author = request.user
        super().save_model(request, obj, form, change)

    # --- Workflow actions (visible as buttons in the changelist) ---

    @admin.action(description='Publicar páginas seleccionadas')
    def action_publish(self, request, queryset):
        for page in queryset:
            page.publish()
        self.message_user(request, f'{queryset.count()} página(s) publicada(s).')

    @admin.action(description='Archivar páginas seleccionadas')
    def action_archive(self, request, queryset):
        for page in queryset:
            page.archive()
        self.message_user(request, f'{queryset.count()} página(s) archivada(s).')

    @admin.action(description='Volver a Borrador')
    def action_revert_to_draft(self, request, queryset):
        for page in queryset:
            page.revert_to_draft()
        self.message_user(request, f'{queryset.count()} página(s) vueltas a borrador.')

    actions = ['action_publish', 'action_archive', 'action_revert_to_draft']
