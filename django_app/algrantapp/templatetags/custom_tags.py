from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def increase_index(context):
    index = context.get('index', 0)
    if index >= len(context['sponsors']) - 1:
        context['index'] = 0
    else:
        context['index'] = index + 1
    return ''