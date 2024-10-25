from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def increase_index(context):
    index = context.get('index', 0)
    if index < len(context['sponsors']):
        context['index'] = index + 1
    else:
        context['index'] = 0
    return context['index']