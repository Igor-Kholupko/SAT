from django.template.defaulttags import register


@register.filter
def get_task_variant(user, task):
    qs = task.taskvariant_set.filter(assignee=user)
    return qs.first if qs.exists() else None


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(is_safe=False)
def sub(value, arg):
    """Add the arg to the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ''
