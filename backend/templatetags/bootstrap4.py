from django import template
from django.contrib.messages import constants as message_constants
from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
register = template.Library()

MESSAGE_LEVEL_CLASSES = {
    DEFAULT_MESSAGE_LEVELS.DEBUG: "alert alert-warning",
    DEFAULT_MESSAGE_LEVELS.INFO: "alert alert-info",
    DEFAULT_MESSAGE_LEVELS.SUCCESS: "alert alert-success",
    DEFAULT_MESSAGE_LEVELS.WARNING: "alert alert-warning",
    DEFAULT_MESSAGE_LEVELS.ERROR: "alert alert-danger",
}

@register.filter
def bootstrap_message_classes(message):
    """
    Return the message classes for a message
    """
    extra_tags = None
    try:
        extra_tags = message.extra_tags
    except AttributeError:
        pass
    if not extra_tags:
        extra_tags = ""
    classes = [extra_tags]
    try:
        level = message.level
    except AttributeError:
        pass
    else:
        try:
            classes.append(MESSAGE_LEVEL_CLASSES[level])
        except KeyError:
            classes.append("alert alert-danger")
    return ' '.join(classes).strip()