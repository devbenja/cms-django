"""
Testimonial list view.
"""
from django.shortcuts import render

from .models import Testimonial


def testimonial_list(request):
    testimonials = Testimonial.objects.filter(is_published=True).select_related('related_work', 'related_work__cover_photo')
    return render(request, 'testimonials/testimonial_list.html', {'testimonials': testimonials})
