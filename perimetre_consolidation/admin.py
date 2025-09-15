from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import PerimetreConso, PerimetreConsoSociete
from comptabilite.admin import AdminLabelMixin
from comptabilite.models import Societe


@admin.register(PerimetreConso)
class PerimetreConsoAdmin(AdminLabelMixin, admin.ModelAdmin):
    list_display = ['id', 'code', 'libelle', 'display_name', 'societes_count', 'manage_societes_link']
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
    
    def societes_count(self, obj):
        """Affiche le nombre de sociétés liées"""
        return obj.get_societes().count()
    societes_count.short_description = "Nb Sociétés"
    societes_count.admin_order_field = 'id'
    
    def manage_societes_link(self, obj):
        """Lien pour gérer les sociétés"""
        url = reverse('admin:perimetre_consolidation_perimetreconso_societes', args=[obj.pk])
        return f'<a href="{url}">Gérer les sociétés</a>'
    manage_societes_link.short_description = "Sociétés"
    manage_societes_link.allow_tags = True
    
    def get_urls(self):
        """Ajouter les URLs personnalisées"""
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/societes/', self.admin_site.admin_view(self.manage_societes_view), name='perimetre_consolidation_perimetreconso_societes'),
        ]
        return custom_urls + urls
    
    def manage_societes_view(self, request, object_id):
        """Vue pour gérer les sociétés d'un périmètre"""
        perimetre = self.get_object(request, object_id)
        if not perimetre:
            messages.error(request, 'Périmètre non trouvé')
            return redirect('admin:perimetre_consolidation_perimetreconso_changelist')
        
        # Récupérer les sociétés liées et disponibles
        societes_liees = perimetre.get_societes()
        societes_disponibles = Societe.objects.exclude(id__in=societes_liees.values_list('id', flat=True))
        
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'add':
                societe_id = request.POST.get('societe_id')
                if societe_id:
                    try:
                        societe = Societe.objects.get(id=societe_id)
                        # Créer la relation (nécessite une requête SQL directe)
                        from django.db import connection
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "INSERT INTO T_J_PEC_SOC (PEC_Id, SOC_Id) VALUES (?, ?)",
                                [perimetre.id, societe.id]
                            )
                        messages.success(request, f'Société {societe.nom} ajoutée au périmètre')
                    except Societe.DoesNotExist:
                        messages.error(request, 'Société non trouvée')
                    except Exception as e:
                        messages.error(request, f'Erreur lors de l\'ajout: {str(e)}')
            
            elif action == 'remove':
                societe_id = request.POST.get('societe_id')
                if societe_id:
                    try:
                        # Supprimer la relation
                        from django.db import connection
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "DELETE FROM T_J_PEC_SOC WHERE PEC_Id = ? AND SOC_Id = ?",
                                [perimetre.id, societe_id]
                            )
                        messages.success(request, 'Société retirée du périmètre')
                    except Exception as e:
                        messages.error(request, f'Erreur lors de la suppression: {str(e)}')
            
            return redirect('admin:perimetre_consolidation_perimetreconso_societes', object_id=object_id)
        
        context = {
            'title': f'Gérer les sociétés - {perimetre.get_display_name()}',
            'perimetre': perimetre,
            'societes_liees': societes_liees,
            'societes_disponibles': societes_disponibles,
            'opts': self.model._meta,
            'has_change_permission': True,
        }
        
        return render(request, 'admin/perimetre_consolidation/perimetreconso/societes.html', context)
    
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


# Le modèle PerimetreConsoSociete n'a pas de clé primaire et ne peut pas être géré par l'admin Django
# La gestion se fait via la vue personnalisée dans PerimetreConsoAdmin
