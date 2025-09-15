from django.db import models


class AdminText(models.Model):
    """Libellés paramétrables pour l'admin (titres, sections, modèles)."""
    language = models.CharField(max_length=5, default='fr', verbose_name="Langue")
    key = models.CharField(max_length=100, verbose_name="Clé")
    value = models.CharField(max_length=255, verbose_name="Valeur")
    display_order = models.IntegerField(default=0, db_column='ADT_DisplayOrder', verbose_name="Ordre d'affichage")

    class Meta:
        db_table = 'T_E_AdminText_ADT'
        unique_together = ('language', 'key')
        verbose_name = 'Libellé Admin'
        verbose_name_plural = 'Libellés Admin'
        ordering = ['language', 'display_order', 'key']

    def __str__(self) -> str:
        return f"{self.language}:{self.key} -> {self.value}"