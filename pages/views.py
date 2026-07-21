"""
Page views: detail view for a Page identified by slug. Returns 404 if draft/archived
or if the slug doesn't exist.
"""
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Page, PageStatus


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, status=PageStatus.PUBLISHED)
    
    if slug == 'contacto' and request.method == 'POST':
        return handle_contact_form(request, page)
    
    return render(request, 'pages/page_detail.html', {'page': page})


def handle_contact_form(request, page):
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()
    
    if not all([name, email, message]):
        messages.error(request, 'Por favor completa todos los campos obligatorios.')
        return render(request, 'pages/page_detail.html', {'page': page})
    
    # Send email
    email_subject = f'Contacto web: {subject or "Consulta general"} - {name}'
    email_body = f"""
Nuevo mensaje de contacto desde la web:

Nombre: {name}
Email: {email}
Teléfono: {phone}
Asunto: {subject}

Mensaje:
{message}
"""
    try:
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_RECIPIENT_EMAIL],
            fail_silently=False,
        )
        messages.success(request, '¡Gracias! Tu mensaje ha sido enviado correctamente. Te contactaremos pronto.')
    except Exception:
        messages.error(request, 'Hubo un error al enviar el mensaje. Por favor intenta de nuevo o contáctanos directamente.')
    
    return redirect('page-contact')
