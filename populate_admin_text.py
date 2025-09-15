#!/usr/bin/env python
"""
Script pour alimenter la table AdminText avec les libellés de la section Référentiel
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'port_adhoc_compta.settings')
django.setup()

from parametres.models import AdminText

def populate_referentiel_labels():
    """Alimenter la table AdminText avec les libellés de la section Référentiel"""
    
    # Libellés pour la section Référentiel
    referentiel_labels = [
        # Section Référentiel
        ('fr', 'app_referentiel', 'Référentiel', 10),
        ('en', 'app_referentiel', 'Reference', 10),
        ('es', 'app_referentiel', 'Referencia', 10),
        ('de', 'app_referentiel', 'Referenz', 10),
        
        # Modèle Periode
        ('fr', 'model_periode', 'Période', 11),
        ('en', 'model_periode', 'Period', 11),
        ('es', 'model_periode', 'Período', 11),
        ('de', 'model_periode', 'Zeitraum', 11),
        
        # Champs Periode
        ('fr', 'field_periode_id', 'ID', 12),
        ('en', 'field_periode_id', 'ID', 12),
        ('es', 'field_periode_id', 'ID', 12),
        ('de', 'field_periode_id', 'ID', 12),
        
        ('fr', 'field_periode_date', 'Date', 13),
        ('en', 'field_periode_date', 'Date', 13),
        ('es', 'field_periode_date', 'Fecha', 13),
        ('de', 'field_periode_date', 'Datum', 13),
        
        ('fr', 'field_periode_annee', 'Année', 14),
        ('en', 'field_periode_annee', 'Year', 14),
        ('es', 'field_periode_annee', 'Año', 14),
        ('de', 'field_periode_annee', 'Jahr', 14),
        
        ('fr', 'field_periode_mois', 'Mois', 15),
        ('en', 'field_periode_mois', 'Month', 15),
        ('es', 'field_periode_mois', 'Mes', 15),
        ('de', 'field_periode_mois', 'Monat', 15),
        
        ('fr', 'field_periode_trimestre_civil', 'Trimestre Civil', 16),
        ('en', 'field_periode_trimestre_civil', 'Civil Quarter', 16),
        ('es', 'field_periode_trimestre_civil', 'Trimestre Civil', 16),
        ('de', 'field_periode_trimestre_civil', 'Bürgerliches Quartal', 16),
        
        # Actions admin
        ('fr', 'action_periode_add', 'Ajouter une période', 17),
        ('en', 'action_periode_add', 'Add period', 17),
        ('es', 'action_periode_add', 'Agregar período', 17),
        ('de', 'action_periode_add', 'Zeitraum hinzufügen', 17),
        
        ('fr', 'action_periode_change', 'Modifier la période', 18),
        ('en', 'action_periode_change', 'Change period', 18),
        ('es', 'action_periode_change', 'Cambiar período', 18),
        ('de', 'action_periode_change', 'Zeitraum ändern', 18),
        
        ('fr', 'action_periode_delete', 'Supprimer la période', 19),
        ('en', 'action_periode_delete', 'Delete period', 19),
        ('es', 'action_periode_delete', 'Eliminar período', 19),
        ('de', 'action_periode_delete', 'Zeitraum löschen', 19),
        
        # Messages
        ('fr', 'message_periode_created', 'Période créée avec succès', 20),
        ('en', 'message_periode_created', 'Period created successfully', 20),
        ('es', 'message_periode_created', 'Período creado con éxito', 20),
        ('de', 'message_periode_created', 'Zeitraum erfolgreich erstellt', 20),
        
        ('fr', 'message_periode_updated', 'Période mise à jour avec succès', 21),
        ('en', 'message_periode_updated', 'Period updated successfully', 21),
        ('es', 'message_periode_updated', 'Período actualizado con éxito', 21),
        ('de', 'message_periode_updated', 'Zeitraum erfolgreich aktualisiert', 21),
        
        ('fr', 'message_periode_deleted', 'Période supprimée avec succès', 22),
        ('en', 'message_periode_deleted', 'Period deleted successfully', 22),
        ('es', 'message_periode_deleted', 'Período eliminado con éxito', 22),
        ('de', 'message_periode_deleted', 'Zeitraum erfolgreich gelöscht', 22),
    ]
    
    # Supprimer les anciens libellés pour la section Référentiel
    AdminText.objects.filter(key__startswith='app_referentiel').delete()
    AdminText.objects.filter(key__startswith='model_periode').delete()
    AdminText.objects.filter(key__startswith='field_periode_').delete()
    AdminText.objects.filter(key__startswith='action_periode_').delete()
    AdminText.objects.filter(key__startswith='message_periode_').delete()
    
    # Créer les nouveaux libellés
    created_count = 0
    for language, key, value, display_order in referentiel_labels:
        admin_text, created = AdminText.objects.get_or_create(
            language=language,
            key=key,
            defaults={
                'value': value,
                'display_order': display_order
            }
        )
        if created:
            created_count += 1
        else:
            # Mettre à jour si existe déjà
            admin_text.value = value
            admin_text.display_order = display_order
            admin_text.save()
    
    print(f"✅ {created_count} libellés créés/mis à jour pour la section Référentiel")
    print(f"📊 Total des libellés dans la base : {AdminText.objects.count()}")

if __name__ == '__main__':
    populate_referentiel_labels()
