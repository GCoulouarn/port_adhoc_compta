from django.contrib import admin
from .models import PerimetreConso
from comptabilite.admin import AdminLabelMixin


@admin.register(PerimetreConso)
class PerimetreConsoAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'code', 'libelle', 'display_name']
    list_filter = ['code']
    search_fields = ['code', 'libelle']
    ordering = ['code', 'libelle']
    list_display_links = ['id', 'code']
    list_editable = ['libelle']
    
    def display_name(self, obj):
        """Affiche le nom complet du périmètre"""
        return obj.get_display_name()
    display_name.short_description = "Nom complet"
    display_name.admin_order_field = 'code'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('id', 'code', 'libelle'),
            'description': 'Informations de base du périmètre de consolidation'
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Override pour appliquer les libellés dynamiques"""
        # Appliquer les libellés dynamiques
        self.model.apply_dynamic_labels()
        return super().changelist_view(request, extra_context)
