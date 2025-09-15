from django.db import models
from comptabilite.dynamic_labels import DynamicLabelsMixin


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
