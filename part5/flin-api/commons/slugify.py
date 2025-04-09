from django.utils.text import slugify as _slugify
import re

def _base_slugify(model_objects, slug_field, string):
    slug = _slugify(string)

    existing_slugs = model_objects.filter(
        **{f"{slug_field}__startswith": slug}
    ).values_list(slug_field, flat=True)

    if slug not in existing_slugs:
        return slug

    slug_pattern = re.compile(rf"^{re.escape(slug)}-(\d+)$")

    suffixes = [
        int(match.group(1)) for s in existing_slugs if (match := slug_pattern.match(s))
    ]

    next_suffix = max(suffixes, default=1) + 1

    return f"{slug}-{next_suffix}"

def slugify(model, slug_field, string):
    return _base_slugify(model.objects, slug_field, string)

def slugify_deleted(model, slug_field, string):
    return _base_slugify(model.all_objects, slug_field, f"deleted-{string}")