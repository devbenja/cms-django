"""
Block types for rich content (used by Page.body and PortfolioWork.body).
Each block is a dict with a 'type' key and its own schema.
HTML inside paragraph/quote is sanitized with bleach on save.
"""
import bleach
from django.core.exceptions import ValidationError


# --- Block type schemas (used by the editor and renderer) ---

BLOCK_TYPES = [
    'heading',
    'paragraph',
    'image',
    'cta',
    'quote',
    'list',
    'gallery',
    'video_embed',
]

# HTML allowed inside paragraph / quote / list
ALLOWED_TAGS = [
    'a', 'b', 'i', 'em', 'strong', 'br', 'p', 'span', 'ul', 'ol', 'li',
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'span': ['class'],
}


def sanitize_html(text: str) -> str:
    """Strip everything except a small whitelist of inline tags."""
    if not text:
        return ''
    return bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )


def validate_blocks(blocks):
    """Basic structural validation: each item must be a dict with 'type' in BLOCK_TYPES."""
    if not isinstance(blocks, list):
        raise ValidationError('El contenido debe ser una lista de bloques.')
    for i, block in enumerate(blocks):
        if not isinstance(block, dict):
            raise ValidationError(f'Bloque #{i + 1}: debe ser un objeto.')
        block_type = block.get('type')
        if block_type not in BLOCK_TYPES:
            raise ValidationError(f'Bloque #{i + 1}: tipo "{block_type}" no permitido.')
    return blocks


def sanitize_blocks(blocks):
    """Run sanitize_html on text-bearing fields. Returns the cleaned list."""
    if not isinstance(blocks, list):
        return blocks
    cleaned = []
    for block in blocks:
        if not isinstance(block, dict):
            cleaned.append(block)
            continue
        b = dict(block)
        if b.get('type') == 'paragraph' and 'text' in b:
            b['text'] = sanitize_html(b['text'])
        elif b.get('type') == 'quote' and 'text' in b:
            b['text'] = sanitize_html(b['text'])
        elif b.get('type') == 'list' and 'items' in b and isinstance(b['items'], list):
            b['items'] = [sanitize_html(str(item)) for item in b['items']]
        cleaned.append(b)
    return cleaned
