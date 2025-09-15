from django.contrib import admin
from .models import Periode
from comptabilite.admin import AdminLabelMixin


@admin.register(Periode)
class PeriodeAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'periode_display', 'trimestre_display', 'date']
    list_filter = ['annee', 'mois', 'trimestre_civil']
    search_fields = ['annee', 'mois']
    ordering = ['annee', 'mois']
    list_display_links = ['id', 'periode_display']
    list_editable = ['date']
    
    def periode_display(self, obj):
        """Affiche la période formatée dans la liste"""
        return obj.get_periode_display()
    periode_display.short_description = "Période"
    periode_display.admin_order_field = 'annee'
    
    def trimestre_display(self, obj):
        """Affiche le trimestre dans la liste"""
        return obj.get_trimestre_display()
    trimestre_display.short_description = "Trimestre"
    trimestre_display.admin_order_field = 'trimestre_civil'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('id', 'date', 'annee', 'mois', 'trimestre_civil'),
            'description': 'Informations de base de la période'
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Override pour appliquer les libellés dynamiques"""
        # Appliquer les libellés dynamiques
        self.model.apply_dynamic_labels()
        return super().changelist_view(request, extra_context)
