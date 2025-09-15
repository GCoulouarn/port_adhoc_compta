from django.contrib import admin
from .models import PerimetreConso, PerimetreConsoSociete
from comptabilite.admin import AdminLabelMixin


class PerimetreConsoSocieteInline(admin.TabularInline):
    model = PerimetreConsoSociete
    extra = 0
    fields = ['societe']
    autocomplete_fields = ['societe']
    verbose_name = "Société"
    verbose_name_plural = "Sociétés liées"


@admin.register(PerimetreConso)
class PerimetreConsoAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'code', 'libelle', 'display_name', 'societes_count']
    list_filter = ['code']
    search_fields = ['code', 'libelle']
    ordering = ['code', 'libelle']
    list_display_links = ['id', 'code']
    list_editable = ['libelle']
    inlines = [PerimetreConsoSocieteInline]
    
    def display_name(self, obj):
        """Affiche le nom complet du périmètre"""
        return obj.get_display_name()
    display_name.short_description = "Nom complet"
    display_name.admin_order_field = 'code'
    
    def societes_count(self, obj):
        """Affiche le nombre de sociétés liées"""
        return obj.get_societes().count()
    societes_count.short_description = "Nb Sociétés"
    societes_count.admin_order_field = 'id'
    
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


@admin.register(PerimetreConsoSociete)
class PerimetreConsoSocieteAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['perimetre_conso', 'societe']
    list_filter = ['perimetre_conso', 'societe']
    search_fields = ['perimetre_conso__code', 'perimetre_conso__libelle', 'societe__nom']
    autocomplete_fields = ['perimetre_conso', 'societe']
    ordering = ['perimetre_conso', 'societe']
    
    def changelist_view(self, request, extra_context=None):
        """Override pour appliquer les libellés dynamiques"""
        # Appliquer les libellés dynamiques
        self.model.apply_dynamic_labels()
        return super().changelist_view(request, extra_context)
