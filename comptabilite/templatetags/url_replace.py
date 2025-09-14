from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, **kwargs):
    """
    Remplace ou ajoute des paramètres dans l'URL actuelle
    """
    query = request.GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()
