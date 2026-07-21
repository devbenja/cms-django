import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
if not settings.configured:
    import config.settings
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib	contenttypes',
            'accounts',
            'core',
            'pages',
            'portfolio',
            'testimonials',
            'faqs',
        ],
        USE_TZ=True,
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    )
    django.setup()

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from accounts.models import User, Role
from core.models import CoreConfig
from portfolio.models import Category, PortfolioWork, WorkPhoto
from pages.models import Page, PageStatus
from testimonials.models import Testimonial
from faqs.models import FAQCategory, FAQ

User = get_user_model()


class Command(BaseCommand):
    help = 'Poblar la base de datos con contenido de prueba'

    def handle(self, *args, **options):
        # Crear usuario admin
        self.create_admin_user()

        # Configurar configuración del sitio
        self.site_config()

        # Crear categorías de portfolio
        self.create_categories()

        # Crear obras de portfolio
        self.create_portfolio_works()

        # Crear testimonios
        self.create_testimonials()

        # Crear páginas
        self.create_pages()

        # Crear FAQs
        self.create_faqs()

        self.complete()

    def create_admin_user(self):
        """Crear usuario administrador"""
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@constructora.com',
                'first_name': 'Admin',
                'last_name': 'Usuario',
                'is_staff': True,
                'is_superuser': True,
                'role': Role.ADMIN,
                'password': 'admin123.',  # Cambiar después de primer login
            }
        )
        if created:
            admin.set_password('admin123.')
            admin.save()
            self.stdout.write(self.style.SUCCESS('✓ Usuario admin creado (usuario: admin, password: admin123.)'))

        editor, created = User.objects.get_or_create(
            username='editor',
            defaults={
                'email': 'editor@constructora.com',
                'first_name': 'Editor',
                'last_name': 'Usuario',
                'is_staff': True,
                'role': Role.EDITOR,
            }
        )
        if created:
            editor.set_password('editor123.')
            editor.save()
            self.stdout.write(self.style.SUCCESS('✓ Usuario editor creado (usuario: editor, password: editor123.)'))

    def site_config(self):
        """Configurar la core configuration (solo un registro)"""
        config, created = CoreConfig.objects.get_or_create(pk=1)
        
        if created:
            config.update(
                site_name='Constructora Constructora',
                tagline='Construimos sueños, elevando horizontes',
                contact_email='contacto@constructora.com',
                contact_phone='+505 2223-3344',
                contact_whatsapp='5052223344',
                city='Managua',
                department='Managua',
                country='Nicaragua',
                address_line1='Av. de la Independencia',
                address_line2='Edificio Empresarial, Oficina 301',
                facebook_url='https://facebook.com/constructoraconstructora',
                instagram_url='https://instagram.com/constructoraconstructora',
                linkedin_url='https://linkedin.com/company/constructora-constructora',
                google_maps_embed_url='',
            )
            self.stdout.write(self.style.SUCCESS('✓ Configuración del sitio creada'))
        else:
            config.update(
                site_name='Constructora Constructora',
                tagline='Construimos sueños, elevando horizontes',
                contact_email='contacto@constructora.com',
                contact_phone='+505 2223-3344',
                contact_whatsapp='5052223344',
                city='Managua',
                department='Managua',
                country='Nicaragua',
                address_line1='Av. de la Independencia',
                address_line2='Edificio Empresarial, Oficina 301',
                facebook_url='https://facebook.com/constructoraconstructora',
                instagram_url='https://instagram.com/constructoraconstructora',
                linkedin_url='https://linkedin.com/company/constructora-constructora',
                google_maps_embed_url='',
            )
            config.save()
            self.stdout.write(self.style.SUCCESS('✓ Configuración del sitio actualizada'))

    def create_categories(self):
        """Crear categorías de portfolio"""
        categories = [
            ('Edificios y Torres', 'edificios-torres', 'Torres residenciales, comerciales y corporativas de altura'),
            ('Urbanizaciones', 'urbanizaciones', 'Proyectos de desarrollo urbano residencial completo'),
            ('Carreteras e Infraestructura', 'carreteras-infraestructura', 'Proyectos viales, puentes y obras civiles'),
            ('Centros Comerciales', 'centros-comerciales', 'Centros comerciales y plazas de entretenimiento'),
            ('Hospitales y Salas de Emergencia', 'hospitales-emergencia', 'Instalaciones médicas modernas y centros de salud'),
            ('Educación e Instituciones', 'educacion-instituciones', 'Colegios, universidades y centros educativos'),
        ]

        for name, slug, description in categories:
            Category.objects.get_or_create(
                name=name,
                slug=slug,
                defaults={'description': description, 'order': 0}
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {categories[0][0]} - {len(categories)} categorías creadas'))

    def create_portfolio_works(self):
        """Crear obras de portfolio"""
        categories = Category.objects.all()
        works_data = [
            {
                'title': 'Torre Managua Center',
                'client': 'Grupo Managua Desarrollos',
                'location': 'Managua, Nicaragua',
                'year': 2024,
                'category': categories[0],
                'short_desc': 'Torre residencial de 45 pisos con vista panorámica a los volcanes.',
                'is_published': True,
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Urbanización Los Laureles',
                'client': 'Nueva Vida Constructores',
                'location': 'Leon, Nicaragua',
                'year': 2023,
                'category': categories[1],
                'short_desc': 'Comunidad residencial para 500 familias con áreas verdes.',
                'is_published': True,
                'is_featured': True,
                'order': 2,
            },
            {
                'title': 'Puente sobre el Rio Tipitapa',
                'client': 'Ministerio de Obras Públicas',
                'location': 'Managua, Nicaragua',
                'year': 2023,
                'category': categories[2],
                'short_desc': 'Estructura vial que conecta la capital con el sur del país.',
                'is_published': True,
                'is_featured': False,
                'order': 3,
            },
            {
                'title': 'Centro Comercial Plaza Centro',
                'client': 'Investora Centro',
                'location': 'León, Nicaragua',
                'year': 2024,
                'category': categories[3],
                'short_desc': 'Centro comercial de 150 metros con 30 tiendas.',
                'is_published': True,
                'is_featured': True,
                'order': 4,
            },
            {
                'title': 'Hospital San Rafael',
                'client': 'Red de Salud Managua',
                'location': 'Managua, Nicaragua',
                'year': 2022,
                'category': categories[4],
                'short_desc': 'Centro médico con 200 camas y salas de emergencia 24/7.',
                'is_published': True,
                'is_featured': False,
                'order': 5,
            },
            {
                'title': 'Colegio Internacional',
                'client': 'Ministerio de Educación',
                'location': 'Rivas, Nicaragua',
                'year': 2024,
                'category': categories[5],
                'short_desc': 'Complejo educativo con aulas modernas y laboratorios.',
                'is_published': True,
                'is_featured': True,
                'order': 6,
            },
            {
                'title': 'Torre Corporativa Business Park',
                'client': 'Business Park Development',
                'location': 'Managua, Nicaragua',
                'year': 2025,
                'category': categories[0],
                'short_desc': 'Torre corporativa de lujo para empresas multinacionales.',
                'is_published': False,
                'is_featured': False,
                'order': 7,
            },
            {
                'title': 'Urbanización Valle Verde',
                'client': 'Eco Construcciones',
                'location': 'Masaya, Nicaragua',
                'year': 2025,
                'category': categories[1],
                'short_desc': 'Urbanización sustentable con energías renovables.',
                'is_published': True,
                'is_featured': False,
                'order': 8,
            },
        ]

        works_created = []
        for work_data in works_data:
            work, _ = PortfolioWork.objects.get_or_create(
                title=work_data.get('title'),
                slug=work_data.get('title').lower().replace(' ', '-'),
                defaults={
                    'category': work_data['category'],
                    'client': work_data.get('client', ''),
                    'location': work_data['location'],
                    'year': work_data['year'],
                    'description_short': work_data.get('short_desc', ''),
                    'body': [],  # JSON field vacío
                    'is_published': work_data.get('is_published', False),
                    'is_featured': work_data.get('is_featured', False),
                    'order': work_data.get('order', 0),
                }
            )

            if work_id := work.pk:
                works_created.append(work_id)

        self.stdout.write(self.style.SUCCESS(f'✓ {len(works_created)} obras creadas'))

    def create_testimonials(self):
        """Crear testimonios"""
        works = PortfolioWork.objects.filter(is_published=True).order_by('?')[:3]
        testimonials = [
            {
                'client_name': 'María Fernández',
                'client_role': 'Gerente de Proyecto',
                'client_company': 'Grupo Managua',
                'quote': 'Trabajar con Constructora Constructora ha sido una experiencia excepcional. La atención al detalle y el compromiso con los plazos han superado todas mis expectativas.',
                'related_work': works[0] if works.exists() else None,
                'order': 1,
            },
            {
                'client_name': 'Carlos Mendoza',
                'client_role': 'Director de Operaciones',
                'client_company': 'Nueva Vida Constructores',
                'quote': 'Los resultados superaron mis expectativas. La presentación profesional y la atención personalizada han sido claves en nuestra colaboración.',
                'related_work': works[1] if len(works) > 1 else None,
                'order': 2,
            },
            {
                'client_name': 'Ana Torres',
                'client_role': 'Arquitecta Principal',
                'client_company': 'Estudio Torres Arquitectos',
                'quote': 'El diseño y ejecución del proyecto han sido impecables. Son un verdadero profesionalismo en cada detalle.',
                'related_work': works[2] if len(works) > 2 else None,
                'order': 3,
            },
        ]

        for testimonial_data in testimonials:
            Testimonial.objects.get_or_create(
                client_name=testimonial_data['client_name'],
                defaults={
                    'client_role': testimonial_data['client_role'],
                    'client_company': testimonial_data['client_company'],
                    'quote': testimonial_data['quote'],
                    'related_work': testimonial_data['related_work'],
                    'is_published': True,
                    'order': testimonial_data['order'],
                }
            )

        self.stdout.write(self.style.SUCCESS('✓ Testimonios creados'))

    def create_pages(self):
        """Crear páginas corporativas"""
        pages_data = [
            {
                'title': 'Inicio',
                'slug': 'inicio',
                'status': PageStatus.PUBLISHED,
                'body': [],
            },
            {
                'title': 'Quienes Somos',
                'slug': 'quienes-somos',
                'status': PageStatus.PUBLISHED,
                'body': [
                    {'tag': 'h2', 'content': 'Sobre Nosotros'},
                    {'tag': 'html', 'content': '<p>Constructora Constructora lleva más de 25 años construyendo sueños en Nicaragua.</p>'},
                ],
            },
            {
                'title': 'Nuestros Servicios',
                'slug': 'servicios',
                'status': PageStatus.PUBLISHED,
                'body': [
                    {'tag': 'h2', 'content': 'Servicios'},
                    {'tag': 'html', 'content': '<p>Ofrecemos soluciones integrales en construcción residencial, comercial e industrial.</p>'},
                ],
            },
            {
                'title': 'Portafolio',
                'slug': 'portafolio',
                'status': PageStatus.PUBLISHED,
                'body': [],
            },
            {
                'title': 'Contacto',
                'slug': 'contacto',
                'status': PageStatus.PUBLISHED,
                'body': [
                    {'tag': 'h2', 'content': 'Contáctanos'},
                    {'tag': 'html', 'content': '<p>Estamos listos para escuchar tu proyecto. Contáctanos hoy mismo.</p>'},
                ],
            },
        ]

        authors_user = User.objects.filter(is_staff=True).first()
        if not authors_user:
            print('⚠ No se encontró ningún usuario staff registrado.')
            return

        created_count = 0
        for page_data in pages_data:
            page, _ = Page.objects.get_or_create(
                slug=page_data['slug'],
                defaults={
                    'title': page_data['title'],
                    'status': page_data['status'],
                    'body': page_data.get('body', []),
                }
            )
            if page and not page.author_id:
                page.author = authors_user
                page.save()
                if page.pk != page_data['slug']:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f'✓ {created_count} páginas creadas/actualizadas'))

    def create_faqs(self):
        """Crear FAQs"""
        categories_count = FAQCategory.objects.filter(name='General').count()
        if not categories_count:
            FAQCategory.objects.create(name='General', slug='general', order=0)
            FAQCategory.objects.create(name='Proyectos', slug='proyectos', order=1)
            
            faqs = [
                {'category': 'general', 'question': '¿Cuáles son los tiempos de entrega promedio?', 'answer': 'Nuestros proyectos residenciales tienen un tiempo promedio de 12-18 meses, dependiendo del tamaño y complejidad.', 'order': 0},
                {'category': 'general', 'question': '¿Ofrecen financiamiento propio?', 'answer': 'Sí, ofrecemos opciones de financiamiento con plazos flexibles adaptados a tus necesidades.', 'order': 1},
                {'category': 'general', 'question': '¿Pueden trabajar con mi terreno?', 'answer': 'Sí, trabajamos con terrenos adquiridos por el cliente o ofrecemos paquetes llave en mano.', 'order': 2},
                {'category': 'general', 'question': '¿Cómo pueden visitar una obra en construcción?', 'answer': 'Nuestros clientes pueden programar visitas a las obras en la fase de construcción previa cita.', 'order': 3},
                {'category': 'proyectos', 'question': '¿Qué servicios adicionales ofrecen?', 'answer': 'Diseño arquitectónico, gestión de permisos, selección de materiales, supervisione completa, paisajismo y mantenimiento.', 'order': 0},
            ]
            
            for faq_data in faqs:
                FAQ.objects.get_or_create(
                    question=faq_data['question'],
                    defaults={
                        'category_id': faq_data['category'],
                        'answer': faq_data['answer'],
                        'order': faq_data['order'],
                        'is_published': True,
                    }
                )
            self.stdout.write(self.style.SUCCESS('✓ FAQs creadas'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ FAQs existentes (saltando creación)'))

    def complete(self):
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))
        self.stdout.write(self.style.SUCCESS('✅ ¡Base de datos pobrada con éxito!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('\nUsuarios creados:'))
        self.stdout.write(self.style.SUCCESS('  - admin (password: admin123.)'))
        self.stdout.write(self.style.SUCCESS('  - editor (password: editor123.)'))
        self.stdout.write(self.style.SUCCESS('\nPara acceder al panel de administración:'))
        self.stdout.write(self.style.SUCCESS('  - URL: /admin/'))
        self.stdout.write(self.style.SUCCESS('  - Usuario: admin'))
        self.stdout.write(self.style.SUCCESS('  - Contraseña: admin123.'))
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))