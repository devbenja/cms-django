"""
URL configuration for the public site.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from pages import views as pages_views
from portfolio import views as portfolio_views
from testimonials import views as testimonials_views
from faqs import views as faqs_views
from core import views as core_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', core_views.home, name='home'),

    # Friendly slugs (static pages with known URLs)
    path('quienes-somos/', pages_views.page_detail, {'slug': 'quienes-somos'}, name='page-about'),
    path('servicios/', pages_views.page_detail, {'slug': 'servicios'}, name='page-services'),
    path('contacto/', pages_views.page_detail, {'slug': 'contacto'}, name='page-contact'),

    # Generic page (used for any other published Page with a slug)
    path('pagina/<slug:slug>/', pages_views.page_detail, name='detail'),

    # Portfolio
    path('proyectos/', portfolio_views.work_list, name='portfolio_list'),
    path('proyectos/<slug:slug>/', portfolio_views.work_detail, name='portfolio_detail'),

    # Testimonials
    path('testimonios/', testimonials_views.testimonial_list, name='testimonial_list'),

    # FAQs
    path('preguntas-frecuentes/', faqs_views.faq_list, name='faq_list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
