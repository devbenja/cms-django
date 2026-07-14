"""
Testimonials: client quotes shown on the home page and optionally linked to a work.
"""
from django.db import models
from simple_history.models import HistoricalRecords


class Testimonial(models.Model):
    client_name = models.CharField('nombre del cliente', max_length=200)
    client_role = models.CharField('cargo', max_length=200, blank=True,
                                   help_text='Ej: "Gerente de proyecto"')
    client_company = models.CharField('empresa', max_length=200, blank=True)
    client_photo = models.ImageField('foto del cliente', upload_to='testimonials/', blank=True, null=True)
    quote = models.TextField('cita', help_text='La cita textual del cliente.')

    related_work = models.ForeignKey(
        'portfolio.PortfolioWork',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='testimonials',
        verbose_name='obra relacionada',
        help_text='Opcional. Si se borra la obra, el testimonio sobrevive.',
    )

    is_published = models.BooleanField('publicado', default=False)
    order = models.PositiveIntegerField('orden', default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'testimonio'
        verbose_name_plural = 'testimonios'

    def __str__(self):
        return f'{self.client_name} — {self.quote[:60]}'
