import sys
sys.path.insert(0, r'C:\Users\DTEC14\Desktop\BENJA\projects\cms-constructora')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from pages.models import Page

p = Page.objects.get(slug='contacto')

html_form = """<form class="space-y-6" method="post" action="/contacto/">{% csrf_token %}
<div class="grid gap-6 md:grid-cols-2">
<div><label class="block text-sm font-medium text-text-secondary mb-1" for="id_name">Nombre completo</label><input type="text" name="name" id="id_name" class="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent" required></div>
<div><label class="block text-sm font-medium text-text-secondary mb-1" for="id_email">Correo electronico</label><input type="email" name="email" id="id_email" class="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent" required></div>
</div>
<div><label class="block text-sm font-medium text-text-secondary mb-1" for="id_phone">Telefono / WhatsApp</label><input type="tel" name="phone" id="id_phone" class="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent"></div>
<div><label class="block text-sm font-medium text-text-secondary mb-1" for="id_subject">Asunto</label><select name="subject" id="id_subject" class="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent"><option value="">Selecciona una opcion</option><option value="cotizacion">Solicitud de cotizacion</option><option value="informacion">Informacion general</option><option value="trabaja">Trabaja con nosotros</option><option value="otro">Otro</option></select></div>
<div><label class="block text-sm font-medium text-text-secondary mb-1" for="id_message">Mensaje</label><textarea name="message" id="id_message" rows="5" class="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent" required></textarea></div>
<button type="submit" class="w-full md:w-auto px-8 py-3 bg-brand-primary text-white font-medium rounded-lg hover:bg-brand-primary/90 transition-colors">Enviar mensaje</button>
</form>"""

html_info = """<div class="grid gap-4 md:grid-cols-3 mt-8">
<div class="p-6 bg-surface border border-border rounded-xl"><h4 class="font-semibold text-primary mb-2">Oficina Principal</h4><p class="text-text-secondary">Av. de la Independencia<br>Edificio Empresarial, Oficina 301<br>Managua, Nicaragua</p></div>
<div class="p-6 bg-surface border border-border rounded-xl"><h4 class="font-semibold text-primary mb-2">Telefonos</h4><p class="text-text-secondary">+505 2223-3344<br>+505 8888-7777 (WhatsApp)</p></div>
<div class="p-6 bg-surface border border-border rounded-xl"><h4 class="font-semibold text-primary mb-2">Email</h4><p class="text-text-secondary">contacto@constructora.com<br>ventas@constructora.com</p></div>
</div>"""

p.body = [
    {'type': 'heading', 'level': 2, 'text': 'Contactanos'},
    {'type': 'paragraph', 'text': 'Estamos listos para escuchar tu proyecto. Completa el formulario y nos pondremos en contacto contigo en menos de 24 horas.'},
    {'type': 'html', 'text': html_form},
    {'type': 'heading', 'level': 3, 'text': 'Informacion de Contacto'},
    {'type': 'html', 'text': html_info},
]
p.save()
print('Contacto actualizado correctamente')