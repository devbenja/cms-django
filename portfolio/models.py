"""
Portfolio: portfolio of works (edificios, carreteras, urbanizaciones) with
a photo gallery per work.
"""
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from core.blocks import sanitize_blocks, validate_blocks


class Category(models.Model):
    name = models.CharField('nombre', max_length=100)
    slug = models.SlugField('slug', max_length=100, unique=True)
    description = models.TextField('descripción', blank=True)
    order = models.PositiveIntegerField('orden', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.name


class PortfolioWork(models.Model):
    title = models.CharField('título', max_length=200)
    slug = models.SlugField('slug', max_length=200, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='works',
        verbose_name='categoría',
    )
    client = models.CharField('cliente', max_length=200, blank=True,
                              help_text='Opcional. A veces el cliente es confidencial.')
    location = models.CharField('ubicación', max_length=200, help_text='Ej: "Managua, Nicaragua"')
    year = models.PositiveIntegerField('año')

    description_short = models.CharField(
        'descripción corta', max_length=300, blank=True,
        help_text='Para cards y listados. Máximo 300 caracteres.',
    )
    body = models.JSONField('contenido', default=list, blank=True,
                            help_text='Bloques de contenido reusables (mismos que las páginas).')

    cover_photo = models.ForeignKey(
        'WorkPhoto',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+',
        verbose_name='foto de portada',
        help_text='Si está vacía, se usa la primera foto de la galería.',
    )

    is_published = models.BooleanField('publicado', default=False)
    is_featured = models.BooleanField('destacado en home', default=False)
    order = models.PositiveIntegerField('orden', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['-year', 'order', 'title']
        verbose_name = 'obra'
        verbose_name_plural = 'obras'

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        validate_blocks(self.body or [])

    def save(self, *args, **kwargs):
        self.body = sanitize_blocks(self.body or [])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio:detail', kwargs={'slug': self.slug})

    @property
    def display_cover(self):
        """Returns the cover photo, or the first gallery photo, or None."""
        if self.cover_photo:
            return self.cover_photo
        first = self.photos.order_by('order').first()
        return first


class WorkPhoto(models.Model):
    work = models.ForeignKey(
        PortfolioWork,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='obra',
    )
    image = models.ImageField('imagen', upload_to='portfolio/%Y/%m/')
    caption = models.CharField('pie de foto', max_length=200, blank=True)
    alt_text = models.CharField('texto alternativo', max_length=200,
                                help_text='Requerido para accesibilidad. Describe la imagen.')
    order = models.PositiveIntegerField('orden', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'foto de obra'
        verbose_name_plural = 'fotos de obra'

    def __str__(self):
        return f'{self.work.title} - {self.alt_text or self.image.name}'
