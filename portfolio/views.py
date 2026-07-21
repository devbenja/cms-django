"""
Portfolio views: list of works and detail of a single work.
"""
import json

from django.shortcuts import get_object_or_404, render

from .models import PortfolioWork, WorkPhoto


def work_list(request):
    works = PortfolioWork.objects.filter(is_published=True).select_related('category', 'cover_photo')
    return render(request, 'portfolio/work_list.html', {'works': works})


def work_detail(request, slug):
    work = get_object_or_404(
        PortfolioWork.objects.select_related('category', 'cover_photo'),
        slug=slug,
        is_published=True,
    )
    photos = list(work.photos.all().order_by('order', 'id'))
    # Cross-sell: up to 3 other published works in the same category
    other_works = (
        PortfolioWork.objects
        .filter(is_published=True, category=work.category)
        .exclude(pk=work.pk)
        .select_related('cover_photo')
        .order_by('-year')[:3]
    )

    # Photos serialized for the Alpine.js lightbox
    photos_json = json.dumps([
        {'url': p.image.url, 'alt': p.alt_text, 'caption': p.caption}
        for p in photos
    ])

    return render(request, 'portfolio/work_detail.html', {
        'work': work,
        'photos': photos,
        'other_works': other_works,
        'photos_json': photos_json,
    })
