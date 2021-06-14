from django import template
register = template.Library()

@register.filter(name = 'get_at_index')
def get_at_index(list, index):
    print("\n\nin get_At_index  list = ", list,"  index = ", index)
    return list[index]
