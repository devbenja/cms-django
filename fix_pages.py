import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from pages.models import Page

# Fix Quienes Somos
p = Page.objects.get(slug='quienes-somos')
p.body = [
    {'type': 'heading', 'level': 2, 'text': 'Sobre Nosotros'},
    {'type': 'paragraph', 'text': '<strong>Constructora Constructora</strong> nace en 1998 con la visión de transformar el paisaje urbano de Nicaragua mediante proyectos de construcción que combinan excelencia técnica, diseño innovador y responsabilidad social.'},
    {'type': 'heading', 'level': 3, 'text': 'Nuestra Misión'},
    {'type': 'paragraph', 'text': 'Entregar proyectos de construcción que superen las expectativas de nuestros clientes, generando valor sostenible para las comunidades donde operamos, a través de la excelencia técnica, la innovación constante y el compromiso ético.'},
    {'type': 'heading', 'level': 3, 'text': 'Nuestra Visión'},
    {'type': 'paragraph', 'text': 'Ser la constructora de referencia en Centroamérica, reconocida por la calidad de nuestras obras, la integridad de nuestro equipo y el impacto positivo de nuestros proyectos en el desarrollo de la región.'},
    {'type': 'heading', 'level': 3, 'text': 'Valores Corporativos'},
    {'type': 'html', 'text': '<ul><li><strong>Integridad:</strong> Transparencia en cada proceso y decisión.</li><li><strong>Excelencia:</strong> Superación continua en calidad técnica y servicio.</li><li><strong>Innovación:</strong> Adopción de nuevas tecnologías y metodologías constructivas.</li><li><strong>Responsabilidad:</strong> Compromiso ambiental y social en cada proyecto.</li><li><strong>Colaboración:</strong> Trabajo en equipo y alianzas estratégicas duraderas.</li></ul>'},
    {'type': 'heading', 'level': 3, 'text': 'Nuestra Trayectoria'},
    {'type': 'paragraph', 'text': 'Más de <strong>25 años</strong> de experiencia nos respaldan. Hemos entregado más de <strong>150 proyectos</strong> entre residenciales, comerciales, institucionales e infraestructura vial, consolidándonos como un referente del sector construcción en Nicaragua.'},
]
p.save()
print('Quienes Somos actualizado')

# Fix Servicios
p = Page.objects.get(slug='servicios')
p.body = [
    {'type': 'heading', 'level': 2, 'text': 'Nuestros Servicios'},
    {'type': 'paragraph', 'text': 'Ofrecemos soluciones integrales en construcción, abarcando todo el ciclo de vida del proyecto: desde la concepción y diseño hasta la entrega llave en mano y el mantenimiento posterior.'},
    {'type': 'heading', 'level': 3, 'text': 'Construcción Residencial'},
    {'type': 'html', 'text': '<ul><li>Viviendas unifamiliares de alto standing</li><li>Conjuntos habitacionales y urbanizaciones</li><li>Remodelaciones y ampliaciones</li><li>Diseño arquitectónico personalizado</li></ul>'},
    {'type': 'heading', 'level': 3, 'text': 'Construcción Comercial e Industrial'},
    {'type': 'html', 'text': '<ul><li>Centros comerciales y plazas de entretenimiento</li><li>Edificios de oficinas y corporativos</li><li>Naves industriales y bodegas logísticas</li><li>Hoteles y complejos turísticos</li></ul>'},
    {'type': 'heading', 'level': 3, 'text': 'Infraestructura y Obra Civil'},
    {'type': 'html', 'text': '<ul><li>Carreteras, puentes y viaductos</li><li>Sistemas de agua potable y alcantarillado</li><li>Obras de drenaje y control de inundaciones</li><li>Urbanización vial y señalización</li></ul>'},
    {'type': 'heading', 'level': 3, 'text': 'Edificios Institucionales y de Salud'},
    {'type': 'html', 'text': '<ul><li>Hospitales, clínicas y centros de salud</li><li>Instituciones educativas (colegios, universidades)</li><li>Centros gubernamentales y administrativos</li><li>Centros culturales y deportivos</li></ul>'},
    {'type': 'heading', 'level': 3, 'text': 'Servicios Complementarios'},
    {'type': 'html', 'text': '<ul><li><strong>Diseño arquitectónico e ingeniería:</strong> Desde el anteproyecto hasta los planos de detalle.</li><li><strong>Gestión de permisos y licencias:</strong> Tramitación completa ante municipalidades y ministerios.</li><li><strong>Supervisión y control de calidad:</strong> Inspección técnica en todas las etapas.</li><li><strong>Gerenciamiento de proyectos:</strong> Control de costos, plazos y alcance.</li><li><strong>Mantenimiento post-entrega:</strong> Garantía y servicio técnico continuo.</li></ul>'},
    {'type': 'heading', 'level': 3, 'text': 'Metodología de Trabajo'},
    {'type': 'html', 'text': '<ol><li><strong>Diagnóstico y asesoría inicial</strong> - Entendemos tus necesidades y evaluamos factibilidad.</li><li><strong>Diseño y planificación</strong> - Desarrollamos la solución técnica óptima.</li><li><strong>Presupuesto y cronograma</strong> - Transparencia total en costos y tiempos.</li><li><strong>Ejecución y supervisión</strong> - Construcción con control de calidad riguroso.</li><li><strong>Entrega y post-venta</strong> - Puesta en marcha y acompañamiento continuo.</li></ol>'},
]
p.save()
print('Servicios actualizado')

# Fix Contacto
p = Page.objects.get(slug='contacto')
p.body = [
    {'type': 'heading', 'level': 2, 'text': 'Contáctanos'},
    {'type': 'paragraph', 'text': 'Estamos listos para escuchar tu proyecto. Completa el formulario y nos pondremos en contacto contigo en menos de 24 horas.'},
    {'type': 'html', 'text': '<form class="space-y-6" method="post" action="/contacto/">{% csrf_token %}<div class="grid gap-6 md:grid-cols-2"><div><label class="block text-sm font-medium text-text-secondary mb-1" for="id_name">Nombre completo</label><input type="text" name="name" id="id_name" class="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent" required></div><div><label class="block text-sm font-medium text-text-secondary mb-1" for="id_email">Correo electrónico</label><input type="email" name="email" id="id_email" class="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent" required></div></div><div><label class="block text-sm font-medium text-text-secondary mb-1" for="id_phone">Teléfono / WhatsApp</label><input type="tel" name="phone" id="id_phone" class="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent"></div><div><label class="block text-sm font-medium text-text-secondary mb-1" for="id_subject">Asunto</label><select name="subject" id="id_subject" class="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent"><option value="">Selecciona una opción</option><option value="cotizacion">Solicitud de cotización</option><option value="informacion">Información general</option><option value="trabaja">Trabaja con nosotros</option><option value="otro">Otro</option></select></div><div><label class="block text-sm font-medium text-text-secondary mb-1" for="id_message">Mensaje</label><textarea name="message" id="id_message" rows="5" class="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent" required></textarea></div><button type="submit" class="w-full md:w-auto px-8 py-3 bg-brand-primary text-white font-medium rounded-lg hover:bg-brand-primary/90 transition-colors">Enviar mensaje</button></form>'},
    {'type': 'heading', 'level': 3, 'text': 'Información de Contacto'},
    {'type': 'html', 'text': '<div class="grid gap-4 md:grid-cols-3 mt-8"><div class="p-6 bg-surface border border-border rounded-xl"><h4 class="font-semibold text-primary mb-2">Oficina Principal</h4><p class="text-text-secondary">Av. de la Independencia<br>Edificio Empresarial, Oficina 301<br>Managua, Nicaragua</p></div><div class="p-6 bg-surface border border-border rounded-xl"><h4 class="font-semibold text-primary mb-2">Teléfonos</h4><p class="text-text-secondary">+505 2223-3344<br>+505 8888-7777 (WhatsApp)</p></div><div class="p-6 bg-surface border border-border rounded-xl"><h4 class="font-semibold text-primary mb-2">Email</h4><p class="text-text-secondary">contacto@constructora.com<br>ventas@constructora.com</p></div></div>'},
]
p.save()
print('Contacto actualizado')

# Fix Inicio
p = Page.objects.get(slug='inicio')
p.body = [
    {'type': 'heading', 'level': 2, 'text': 'Bienvenidos a Constructora Constructora'},
    {'type': 'paragraph', 'text': 'Con más de 25 años de experiencia, transformamos ideas en realidad construyendo proyectos que perduran en el tiempo.'},
    {'type': 'cta', 'text': 'Ver Portafolio', 'url': '/portafolio/', 'style': 'primary'},
]
p.save()
print('Inicio actualizado')

# Fix Portafolio
p = Page.objects.get(slug='portafolio')
p.body = [
    {'type': 'heading', 'level': 2, 'text': 'Nuestro Portafolio'},
    {'type': 'paragraph', 'text': 'Descubre algunos de los proyectos que han definido nuestra trayectoria. Cada obra refleja nuestro compromiso con la calidad y la excelencia.'},
]
p.save()
print('Portafolio actualizado')

print('¡Todas las páginas actualizadas correctamente!')