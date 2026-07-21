"""
FAQ list view, grouped by category.
"""
from django.shortcuts import render

from .models import FAQCategory


def faq_list(request):
    categories = FAQCategory.objects.prefetch_related('faqs').all()
    # Filter FAQs to only published ones (all categories visible, even if empty)
    for cat in categories:
        cat.published_faqs = cat.faqs.filter(is_published=True)
    return render(request, 'faqs/faq_list.html', {'categories': categories})
