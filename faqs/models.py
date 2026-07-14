"""
FAQs: frequently asked questions, grouped by category.
"""
from django.db import models
from simple_history.models import HistoricalRecords


class FAQCategory(models.Model):
    name = models.CharField('nombre', max_length=100)
    slug = models.SlugField('slug', max_length=100, unique=True)
    order = models.PositiveIntegerField('orden', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'categoría de FAQ'
        verbose_name_plural = 'categorías de FAQ'

    def __str__(self):
        return self.name


class FAQ(models.Model):
    category = models.ForeignKey(
        FAQCategory,
        on_delete=models.PROTECT,
        related_name='faqs',
        verbose_name='categoría',
    )
    question = models.CharField('pregunta', max_length=300)
    answer = models.TextField('respuesta')
    order = models.PositiveIntegerField('orden', default=0)
    is_published = models.BooleanField('publicado', default=True,
                                       help_text='Por defecto sí: si lo creás, querés que se vea.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['category__order', 'order', 'question']
        verbose_name = 'pregunta frecuente'
        verbose_name_plural = 'preguntas frecuentes'

    def __str__(self):
        return self.question
