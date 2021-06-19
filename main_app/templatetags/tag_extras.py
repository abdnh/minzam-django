from django import template
from django.utils.safestring import mark_safe
from ..models import Tag

register = template.Library()

def tag_list(from_obj):
    tag_rels = from_obj.tags.through.objects.filter(**{f'{from_obj.__class__.__name__.lower()}_id': from_obj.id})
    out = []
    for tag_rel in tag_rels:
        tag = Tag.objects.get(pk=tag_rel.tag_id)
        out.append(f'<a href="{ tag.get_absolute_url() }">{ tag.name }</a>')

    return ', '.join(out)


@register.simple_tag(takes_context=True)
def bookmark_tags(context):
    return mark_safe(tag_list(context['bookmark']))

@register.simple_tag(takes_context=True)
def task_tags(context):
    return mark_safe(tag_list(context['task']))
