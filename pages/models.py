"""
Page model: corporate pages (home, about, services, contact, etc.) and the
editorial workflow (draft / published / archived).

Status transitions are handled by methods on the model, not in views, so that
django-simple-history can audit them in one place.
"""
from django.conf import settings
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from core.blocks import sanitize_blocks, validate_blocks


class PageStatus(models.TextChoices):
    DRAFT = 'draft', 'Borrador'
    PUBLISHED = 'published', 'Publicado'
    ARCHIVED = 'archived', 'Archivado'


class Page(models.Model):
    title = models.CharField('título', max_length=200)
    slug = models.SlugField('slug', max_length=200, unique=True,
                            help_text='URL amigable. Ej: "quienes-somos". Se genera automáticamente.')
    status = models.CharField('estado', max_length=20, choices=PageStatus.choices, default=PageStatus.DRAFT)

    # Rich content: list of blocks (see core/blocks.py)
    body = models.JSONField('contenido', default=list, blank=True)

    # SEO
    meta_title = models.CharField('meta título', max_length=200, blank=True,
                                  help_text='Título para SEO. Si está vacío, se usa el título de la página.')
    meta_description = models.TextField('meta descripción', blank=True, max_length=300,
                                        help_text='Descripción para SEO. Máximo 300 caracteres.')
    og_image = models.ImageField('imagen Open Graph', upload_to='pages/og/', blank=True, null=True,
                                 help_text='Imagen para redes sociales. Si está vacía, se usa la por defecto.')

    # Navigation
    is_in_menu = models.BooleanField('mostrar en menú', default=False)
    menu_order = models.PositiveIntegerField('orden en menú', default=0)

    # Authorship
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='pages',
        verbose_name='autor',
    )

    # Timestamps
    published_at = models.DateTimeField('publicado el', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # History
    history = HistoricalRecords()

    class Meta:
        ordering = ['menu_order', 'title']
        verbose_name = 'página'
        verbose_name_plural = 'páginas'

    def __str__(self):
        return self.title

    # --- Workflow methods (transitions live here, not in views) ---

    def publish(self, user=None):
        """Move from draft/archived to published."""
        if self.status == PageStatus.PUBLISHED:
            return
        self.status = PageStatus.PUBLISHED
        self.published_at = timezone.now()
        # Sanitize blocks one more time on publish to be safe
        self.body = sanitize_blocks(self.body)
        self.save()

    def archive(self, user=None):
        """Move from any state to archived."""
        if self.status == PageStatus.ARCHIVED:
            return
        self.status = PageStatus.ARCHIVED
        self.save()

    def revert_to_draft(self, user=None):
        """Move from published/archived back to draft (for corrections)."""
        if self.status == PageStatus.DRAFT:
            return
        self.status = PageStatus.DRAFT
        self.published_at = None
        self.save()

    def clean(self):
        super().clean()
        validate_blocks(self.body or [])

    def save(self, *args, **kwargs):
        # Auto-fill meta_title from title if empty
        if not self.meta_title:
            self.meta_title = self.title
        # Sanitize on every save
        self.body = sanitize_blocks(self.body or [])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('pages:detail', kwargs={'slug': self.slug})
