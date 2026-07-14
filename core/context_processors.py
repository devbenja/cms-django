"""
Context processor to expose the singleton CoreConfig to every template.
Used by the header, footer, contact info, etc.
"""
from .models import CoreConfig


def site_config(request):
    try:
        config = CoreConfig.get_solo()
    except Exception:
        # Avoid breaking template rendering if the DB is not migrated yet.
        config = None
    return {'site_config': config}
