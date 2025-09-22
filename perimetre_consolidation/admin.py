from django.contrib import admin
from .models import PerimetreConso, PerimetreConsoSociete
from comptabilite.admin import AdminLabelMixin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class PerimetreConsoSocieteResource(resources.ModelResource):
    class Meta:
        model = PerimetreConsoSociete
        skip_unchanged = True
        report_skipped = True
        fields = ("id", "perimetre_conso", "societe")


@admin.register(PerimetreConsoSociete)
class PerimetreConsoSocieteAdmin(AdminLabelMixin, ImportExportModelAdmin):
    """Admin pour la table de jointure PerimetreConsoSociete"""
    list_display = ['id', 'perimetre_conso', 'societe']
    list_filter = ['perimetre_conso', 'societe']
    search_fields = ['perimetre_conso__code', 'perimetre_conso__libelle', 'societe__intitule']
    ordering = ['perimetre_conso', 'societe']
    list_display_links = ['id', 'perimetre_conso', 'societe']
    resource_classes = [PerimetreConsoSocieteResource]
    # Ne pas afficher/saisir l'ID dans le formulaire d'ajout/édition
    readonly_fields = ('id',)
    fieldsets = (
        ('Informations générales', {
            'fields': ('perimetre_conso', 'societe'),
            'description': 'Liaison entre périmètre de consolidation et société'
        }),
    )

    def changelist_view(self, request, extra_context=None):
        """Override pour appliquer les libellés dynamiques"""
        # Appliquer les libellés dynamiques
        self.model.apply_dynamic_labels()
        return super().changelist_view(request, extra_context)


class PerimetreConsoResource(resources.ModelResource):
    class Meta:
        model = PerimetreConso
        skip_unchanged = True
        report_skipped = True
        fields = ("id", "code", "libelle")


@admin.register(PerimetreConso)
class PerimetreConsoAdmin(AdminLabelMixin, ImportExportModelAdmin):
    list_display = ['id', 'code', 'libelle', 'display_name', 'societes_count']
    list_filter = ['code']
    search_fields = ['code', 'libelle']
    ordering = ['code', 'libelle']
    list_display_links = ['id', 'code']
    list_editable = ['libelle']
    resource_classes = [PerimetreConsoResource]

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
