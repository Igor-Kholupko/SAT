from django import template

register = template.Library()


@register.filter
def chat_with(obj, user):
    return obj.chat_with(user)
