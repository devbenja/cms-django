"""
Singleton configuration model for site-wide settings.
Only one row is allowed; enforced in save() and seeded via get_solo().
"""
from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords


class CoreConfig(models.Model):
    # Identity
    site_name = models.CharField('nombre del sitio', max_length=100, default='Constructora')
    tagline = models.CharField('eslogan', max_length=200, blank=True)
    logo = models.ImageField('logo', upload_to='core/', blank=True, null=True)
    favicon = models.ImageField('favicon', upload_to='core/', blank=True, null=True)

    # Contact
    contact_email = models.EmailField('email de contacto', blank=True)
    contact_phone = models.CharField('teléfono', max_length=30, blank=True)
    contact_whatsapp = models.CharField('WhatsApp', max_length=30, blank=True,
                                        help_text='Número con código de país, sin signos. Ej: 50588887777')

    # Location
    address_line1 = models.CharField('dirección (línea 1)', max_length=200, blank=True)
    address_line2 = models.CharField('dirección (línea 2)', max_length=200, blank=True)
    city = models.CharField('ciudad', max_length=100, default='Managua')
    department = models.CharField('departamento', max_length=100, default='Managua')
    country = models.CharField('país', max_length=100, default='Nicaragua')
    map_lat = models.DecimalField('latitud', max_digits=9, decimal_places=6, blank=True, null=True)
    map_lng = models.DecimalField('longitud', max_digits=9, decimal_places=6, blank=True, null=True)
    google_maps_embed_url = models.URLField('URL embed de Google Maps', blank=True)

    # Social
    facebook_url = models.URLField('Facebook', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    linkedin_url = models.URLField('LinkedIn', blank=True)
    youtube_url = models.URLField('YouTube', blank=True)

    # Home hero
    hero_title = models.CharField('título del hero', max_length=200, blank=True)
    hero_subtitle = models.TextField('subtítulo del hero', blank=True)
    hero_image = models.ImageField('imagen del hero', upload_to='core/hero/', blank=True, null=True)
    hero_cta_label = models.CharField('texto del CTA', max_length=50, blank=True)
    hero_cta_url = models.CharField('URL del CTA', max_length=200, blank=True)

    # Footer
    footer_text = models.TextField('texto del footer', blank=True)

    # Home stats (la firma del sitio: 4 numeros que transmiten escala)
    stat_years = models.CharField('años de experiencia', max_length=10, blank=True, default='25+',
                                  help_text='Número grande mostrado en el home. Ej: "25+"')
    stat_works = models.CharField('cantidad de obras', max_length=10, blank=True, default='150+',
                                  help_text='Ej: "150+"')
    stat_departments = models.CharField('departamentos', max_length=10, blank=True, default='12',
                                        help_text='Departamentos donde han construido. Ej: "12"')
    stat_km = models.CharField('km construidos', max_length=10, blank=True, default='200+',
                               help_text='Km de carreteras u obras lineales. Ej: "200+"')

    # Home featured gallery: subset of WorkPhoto chosen for the home page
    home_featured_photos = models.ManyToManyField(
        'portfolio.WorkPhoto',
        blank=True,
        related_name='featured_on_home',
        verbose_name='fotos destacadas del home',
        help_text='Fotos seleccionadas de cualquier obra para mostrar en el home.',
    )

    # Timestamps
    updated_at = models.DateTimeField('última actualización', auto_now=True)

    # History
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'configuración del sitio'
        verbose_name_plural = 'configuración del sitio'

    def __str__(self):
        return f'Config: {self.site_name}'

    def save(self, *args, **kwargs):
        # Singleton enforcement
        if self.pk is None and CoreConfig.objects.exists():
            raise ValidationError('Solo puede existir una configuración del sitio. Edita la existente.')
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Returns the singleton instance, creating it on first access."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
