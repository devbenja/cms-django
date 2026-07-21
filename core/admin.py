"""
CoreConfig admin: Singleton. Only one row allowed.
We disable add/delete so the editor can only edit the existing instance.
"""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import CoreConfig


@admin.register(CoreConfig)
class CoreConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'tagline', 'updated_at')
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        # Disable the "Add" button if a row already exists.
        return not CoreConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Never allow deleting the singleton.
        return False

    def changelist_view(self, request, extra_context=None):
        # If no instance exists, redirect to create page; else redirect to its edit page.
        if CoreConfig.objects.exists():
            obj = CoreConfig.get_solo()
            return HttpResponseRedirect(
                reverse('admin:core_coreconfig_change', args=[obj.pk])
            )
        return super().changelist_view(request, extra_context=extra_context)
