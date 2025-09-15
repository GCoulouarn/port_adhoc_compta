from django.db import models
from comptabilite.dynamic_labels import DynamicLabelsMixin


class PerimetreConsoSociete(DynamicLabelsMixin, models.Model):
    """Modèle pour la table de jointure entre périmètres de consolidation et sociétés"""
    perimetre_conso = models.ForeignKey('PerimetreConso', on_delete=models.CASCADE, db_column='PEC_Id', verbose_name="Périmètre Consolidation")
    societe = models.ForeignKey('comptabilite.Societe', on_delete=models.CASCADE, db_column='SOC_Id', verbose_name="Société")

    class Meta:
        db_table = 'T_J_PEC_SOC'
        verbose_name = "Périmètre Consolidation - Société"
        verbose_name_plural = "Périmètres Consolidation - Sociétés"
        unique_together = [['perimetre_conso', 'societe']]
        managed = False  # Table existante, ne pas gérer par Django

    def __str__(self):
        return f"{self.perimetre_conso} - {self.societe}"


class PerimetreConso(DynamicLabelsMixin, models.Model):
    """Modèle pour les périmètres de consolidation - équivalent à T_E_PerimetreConso_PEC"""
    id = models.IntegerField(primary_key=True, db_column='PEC_Id', verbose_name="ID")
    code = models.CharField(max_length=50, null=True, blank=True, db_column='PEC_Code', verbose_name="Code")
    libelle = models.CharField(max_length=255, null=True, blank=True, db_column='PEC_Libelle', verbose_name="Libellé")

    class Meta:
        db_table = 'T_E_PerimetreConso_PEC'
        verbose_name = "Périmètre Consolidation"
        verbose_name_plural = "Périmètres Consolidation"
        ordering = ['code', 'libelle']
        managed = False  # Table existante, ne pas gérer par Django

    def __str__(self):
        if self.code and self.libelle:
            return f"{self.code} - {self.libelle}"
        elif self.code:
            return self.code
        elif self.libelle:
            return self.libelle
        return f"Périmètre {self.id}"

    def get_display_name(self):
        """Retourne l'affichage formaté du périmètre"""
        if self.code and self.libelle:
            return f"{self.code} - {self.libelle}"
        elif self.code:
            return self.code
        elif self.libelle:
            return self.libelle
        return f"Périmètre {self.id}"

    def get_societes(self):
        """Retourne les sociétés liées à ce périmètre de consolidation"""
        from comptabilite.models import Societe
        societe_ids = PerimetreConsoSociete.objects.filter(perimetre_conso=self).values_list('societe_id', flat=True)
        return Societe.objects.filter(id__in=societe_ids)
