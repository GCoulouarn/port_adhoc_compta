from typing import Dict
from django.utils.translation import get_language
from parametres.models import AdminText


def admin_labels(request) -> Dict[str, object]:
    try:
        lang = get_language() or 'fr'
        items = AdminText.objects.filter(language=lang)
        if not items.exists() and lang != 'fr':
            items = AdminText.objects.filter(language='fr')
        mapping = {row.key: row.value for row in items}
        
        # Récupérer les ordres d'affichage
        orders = {}
        for item in items:
            if item.key.startswith('model.') and item.key.endswith('.name_plural'):
                model_name = item.key.split('.')[1].lower()
                orders[model_name] = item.display_order
        
        # Créer la structure imbriquée pour admin_labels.site.title
        nested = {}
        for key, value in mapping.items():
            parts = key.split('.')
            current = nested
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        
        # Ajouter les ordres d'affichage
        nested['model_orders'] = orders
        
        # Conserver aussi les anciennes clés à plat si utilisées
        flat = {f"admin_label_{k.replace('.', '_')}": v for k, v in mapping.items()}
        flat['admin_labels'] = nested
        return flat
    except Exception as e:
        # En cas d'erreur (table n'existe pas, etc.), retourner des valeurs par défaut
        return {
            'admin_labels': {},
            'model_orders': {}
        }


