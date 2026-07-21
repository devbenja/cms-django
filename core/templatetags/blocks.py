"""
Template tags for rendering rich content blocks.
Usage in a template:
    {% load blocks %}
    {% render_blocks page.body %}
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_blocks(blocks):
    """
    Renders a list of block dicts to HTML by including the corresponding
    template from templates/blocks/. Returns a safe string.

    Each block is a dict like:
        {"type": "heading", "level": 2, "text": "Subtítulo"}
    """
    if not blocks:
        return ''

    # We render each block through a single template that uses include
    # with a variable, to avoid one render() call per block.
    from django.template.loader import render_to_string
    output = []
    for block in blocks:
        if not isinstance(block, dict):
            continue
        block_type = block.get('type')
        if not block_type:
            continue
        try:
            html = render_to_string(f'blocks/{block_type}.html', {'block': block})
            output.append(html)
        except Exception:
            # Block type without a template (or broken data): skip silently.
            continue
    return mark_safe(''.join(output))
