from django.utils.translation import get_language
from parametres.models import AdminText


class DynamicLabelsMixin:
    """Mixin pour appliquer les libellés dynamiques aux modèles"""
    
    @classmethod
    def apply_dynamic_labels(cls):
        """Applique les libellés dynamiques au modèle"""
        try:
            # Récupérer les libellés pour la langue courante
            lang = get_language() or 'fr'
            items = AdminText.objects.filter(language=lang)
            if not items.exists() and lang != 'fr':
                items = AdminText.objects.filter(language='fr')
            
            labels = {row.key: row.value for row in items}
            
            # Appliquer les libellés au modèle
            model_name = cls._meta.model_name
            model_class_name = cls.__name__
            
            # Appliquer verbose_name_plural (essayer les deux formats)
            plural_key_lower = f"model.{model_name}.name_plural"
            plural_key_upper = f"model.{model_class_name}.name_plural"
            
            if plural_key_lower in labels:
                cls._meta.verbose_name_plural = labels[plural_key_lower]
            elif plural_key_upper in labels:
                cls._meta.verbose_name_plural = labels[plural_key_upper]
            
            # Appliquer verbose_name (essayer les deux formats)
            single_key_lower = f"model.{model_name}.name_single"
            single_key_upper = f"model.{model_class_name}.name_single"
            
            if single_key_lower in labels:
                cls._meta.verbose_name = labels[single_key_lower]
            elif single_key_upper in labels:
                cls._meta.verbose_name = labels[single_key_upper]
                
        except Exception:
            # En cas d'erreur, garder les libellés par défaut
            pass
