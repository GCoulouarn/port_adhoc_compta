from django.contrib import admin
from django.utils.translation import get_language
from .models import (
    Societe, Stade, NatureCompte, TypeValeur, PlanCompteGroupe,
    PlanCompteLocal, Devise
)

# Configuration des sections de l'admin
admin.site.site_header = "Port Adhoc Compta - Administration"
admin.site.site_title = "Port Adhoc Compta"
admin.site.index_title = "Gestion Comptable"

# Configuration des sections
class ReferentielAdminConfig:
    """Configuration pour la section Référentiel"""
    verbose_name = "Référentiel"
    verbose_name_plural = "Référentiels"
    app_label = "comptabilite"


class AdminLabelMixin:
    """Mixin pour appliquer les libellés dynamiques aux modèles admin"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_dynamic_labels()
    
    def _apply_dynamic_labels(self):
        """Applique les libellés dynamiques au modèle"""
        try:
            from .context_processors import admin_labels
            from django.test import RequestFactory
            
            # Créer une requête factice pour le context processor
            rf = RequestFactory()
            request = rf.get('/')
            labels = admin_labels(request)
            
            # Appliquer les libellés si disponibles
            model_name = self.model._meta.label_lower.split('.')[-1]
            
            # Libellé du modèle (ex: Devise -> Monnaies)
            model_key = f"model.{model_name}.name_plural"
            if model_key in labels.get('admin_labels', {}):
                self.model._meta.verbose_name_plural = labels['admin_labels'][model_key]
            
            # Libellé de la section (ex: comptabilite -> Finance)
            section_key = "section.comptabilite"
            if section_key in labels.get('admin_labels', {}):
                # Stocker le libellé de section pour utilisation ultérieure
                self._section_label = labels['admin_labels'][section_key]
                
        except Exception as e:
            # En cas d'erreur, continuer avec les libellés par défaut
            pass


@admin.register(Societe)
class SocieteAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'code', 'intitule', 'devise_display', 'groupe', 'archive']
    list_filter = ['groupe', 'archive', 'devise']
    search_fields = ['code', 'intitule', 'devise__intitule']
    ordering = ['id']
    list_display_links = ['id', 'code']
    
    def devise_display(self, obj):
        """Affiche l'intitulé de la devise dans la liste"""
        if obj.devise:
            return f"{obj.devise.intitule} ({obj.devise.code_iso})"
        return "-"
    devise_display.short_description = "Devise"
    devise_display.admin_order_field = 'devise'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('code', 'intitule', 'groupe', 'archive')
        }),
        ('Devise', {
            'fields': ('devise',),
            'description': 'Sélectionnez la devise de la société'
        }),
    )


@admin.register(Stade)
class StadeAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'intitule']
    search_fields = ['intitule']
    ordering = ['id']
    list_display_links = ['id', 'intitule']


@admin.register(NatureCompte)
class NatureCompteAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'code', 'intitule']
    search_fields = ['code', 'intitule']
    ordering = ['id']
    list_display_links = ['id', 'code']


@admin.register(TypeValeur)
class TypeValeurAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'code', 'intitule', 'commentaires']
    search_fields = ['code', 'intitule']
    ordering = ['id']
    list_display_links = ['id', 'code']
    list_editable = ['commentaires']


@admin.register(PlanCompteGroupe)
class PlanCompteGroupeAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'code', 'intitule', 'nature_compte']
    list_filter = ['nature_compte']
    search_fields = ['code', 'intitule']
    ordering = ['id']
    list_display_links = ['id', 'code']


@admin.register(PlanCompteLocal)
class PlanCompteLocalAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'compte', 'intitule', 'societe', 'groupe']
    list_filter = ['societe', 'groupe']
    search_fields = ['compte', 'intitule', 'societe__code']
    ordering = ['id']
    list_display_links = ['id', 'compte']


@admin.register(Devise)
class DeviseAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'code_iso', 'intitule', 'sigle']
    search_fields = ['code_iso', 'intitule', 'sigle']
    ordering = ['id']
    list_display_links = ['id', 'code_iso']
    list_editable = ['intitule', 'sigle']
    
    def changelist_view(self, request, extra_context=None):
        """Override pour appliquer les libellés dynamiques"""
        # Appliquer les libellés dynamiques
        self.model.apply_dynamic_labels()
        return super().changelist_view(request, extra_context)



