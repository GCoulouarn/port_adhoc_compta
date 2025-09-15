from django.db import models
from ..dynamic_labels import DynamicLabelsMixin


class Periode(DynamicLabelsMixin, models.Model):
    """Modèle pour les périodes - équivalent à T_R_Periode_PER"""
    id = models.IntegerField(primary_key=True, db_column='PER_Id', verbose_name="ID")
    date = models.DateTimeField(null=True, blank=True, db_column='PER_Date', verbose_name="Date")
    annee = models.IntegerField(null=True, blank=True, db_column='PER_Annee', verbose_name="Année")
    mois = models.IntegerField(null=True, blank=True, db_column='PER_Mois', verbose_name="Mois")
    trimestre_civil = models.IntegerField(null=True, blank=True, db_column='PER_TrimestreCivil', verbose_name="Trimestre Civil")

    class Meta:
        db_table = 'T_R_Periode_PER'
        verbose_name = "Période"
        verbose_name_plural = "Périodes"
        ordering = ['annee', 'mois']
        managed = False  # Table existante, ne pas gérer par Django
        app_label = 'referentiel'  # Appartenir à la section Référentiel

    def __str__(self):
        if self.annee and self.mois:
            return f"{self.annee}-{self.mois:02d}"
        elif self.date:
            return self.date.strftime("%Y-%m")
        return f"Période {self.id}"

    def get_periode_display(self):
        """Retourne l'affichage formaté de la période"""
        if self.annee and self.mois:
            return f"{self.annee}-{self.mois:02d}"
        elif self.date:
            return self.date.strftime("%Y-%m")
        return f"Période {self.id}"

    def get_trimestre_display(self):
        """Retourne l'affichage du trimestre"""
        if self.trimestre_civil:
            return f"T{self.trimestre_civil}"
        return ""
