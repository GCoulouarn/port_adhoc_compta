from django.contrib import admin
from .models import AdminText


@admin.register(AdminText)
class AdminTextAdmin(admin.ModelAdmin):
    list_display = ['language', 'key', 'value', 'display_order']
    list_filter = ['language']
    search_fields = ['key', 'value']
    ordering = ['language', 'display_order', 'key']
    list_display_links = ['key']
    list_editable = ['display_order']
    
    fieldsets = (
        ('Configuration', {
            'fields': ('language', 'key', 'value'),
            'description': 'Configurez les libellés de l\'interface d\'administration'
        }),
        ('Ordre d\'affichage', {
            'fields': ('display_order',),
            'description': 'Contrôlez l\'ordre d\'affichage des modèles dans chaque section (0 = premier)'
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Override pour utiliser un libellé dynamique"""
        # Récupérer le libellé dynamique
        try:
            from parametres.models import AdminText as AdminTextModel
            lang = request.LANGUAGE_CODE or 'fr'
            admin_text = AdminTextModel.objects.filter(
                language=lang, 
                key='model.admintext.name_plural'
            ).first()
            if not admin_text and lang != 'fr':
                admin_text = AdminTextModel.objects.filter(
                    language='fr', 
                    key='model.admintext.name_plural'
                ).first()
            
            if admin_text:
                # Modifier temporairement le verbose_name_plural
                original_verbose_name_plural = self.model._meta.verbose_name_plural
                self.model._meta.verbose_name_plural = admin_text.value
                
                response = super().changelist_view(request, extra_context)
                
                # Restaurer le verbose_name_plural original
                self.model._meta.verbose_name_plural = original_verbose_name_plural
                
                return response
        except Exception:
            pass
        
        return super().changelist_view(request, extra_context)