from django.utils.translation import get_language
from django.apps import apps
from parametres.models import AdminText


class AdminLabelMiddleware:
    """Middleware pour appliquer les libellés dynamiques aux modèles admin"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Appliquer les libellés dynamiques si on est dans l'admin
        if request.path.startswith('/admin/'):
            self._apply_dynamic_labels()
        
        response = self.get_response(request)
        return response
    
    def _apply_dynamic_labels(self):
        """Applique les libellés dynamiques aux modèles"""
        try:
            # Récupérer les libellés pour la langue courante
            lang = get_language() or 'fr'
            items = AdminText.objects.filter(language=lang)
            if not items.exists() and lang != 'fr':
                items = AdminText.objects.filter(language='fr')
            
            labels = {row.key: row.value for row in items}
            
            # Appliquer les libellés à tous les modèles de toutes les applications
            for app_config in apps.get_app_configs():
                for model in app_config.get_models():
                    model_name = model._meta.model_name
                    
                    # Appliquer verbose_name_plural
                    plural_key = f"model.{model_name}.name_plural"
                    if plural_key in labels:
                        model._meta.verbose_name_plural = labels[plural_key]
                    
                    # Appliquer verbose_name
                    single_key = f"model.{model_name}.name_single"
                    if single_key in labels:
                        model._meta.verbose_name = labels[single_key]
                
        except Exception as e:
            # En cas d'erreur, continuer avec les libellés par défaut
            pass
