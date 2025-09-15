from django import template
from parametres.models import AdminText

register = template.Library()

@register.simple_tag
def get_model_orders():
    """Récupère les ordres d'affichage des modèles"""
    try:
        orders = {}
        for admin_text in AdminText.objects.filter(language='fr'):
            if admin_text.key.startswith('model.') and admin_text.key.endswith('.name_plural'):
                model_name = admin_text.key.split('.')[1].lower()
                orders[model_name] = admin_text.display_order
        return orders
    except Exception:
        return {}

@register.filter
def sort_models_by_order(models, app_label):
    """Trie les modèles selon l'ordre défini dans AdminText"""
    try:
        # Récupérer les ordres d'affichage
        orders = get_model_orders()
        
        # Trier les modèles selon l'ordre
        def get_order(model):
            model_name = model.object_name.lower()
            return orders.get(model_name, 999)  # 999 = ordre par défaut (fin de liste)
        
        return sorted(models, key=get_order)
    except Exception:
        return models
