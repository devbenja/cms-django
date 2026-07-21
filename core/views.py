"""
Home view: shows hero, featured works, featured testimonials, and a CTA.
"""
from django.shortcuts import render

from portfolio.models import PortfolioWork
from testimonials.models import Testimonial


def home(request):
    config = None
    try:
        from core.models import CoreConfig
        config = CoreConfig.get_solo()
    except Exception:
        pass

    featured_works = PortfolioWork.objects.filter(is_published=True, is_featured=True)[:3]
    if not featured_works.exists():
        featured_works = PortfolioWork.objects.filter(is_published=True)[:3]

    testimonials = Testimonial.objects.filter(is_published=True)[:3]

    # For the map: count distinct locations
    works_count = PortfolioWork.objects.filter(is_published=True).values('location').distinct().count()

    context = {
        'site_config': config,
        'featured_works': featured_works,
        'testimonials': testimonials,
        'works_count': works_count,
    }
    return render(request, 'core/home.html', context)
