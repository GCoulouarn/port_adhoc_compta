from django.db import models
from django.contrib.auth.models import User
from .dynamic_labels import DynamicLabelsMixin


class Societe(models.Model):
    """Modèle pour les sociétés - équivalent à T_E_Societe_SOC"""
    id = models.IntegerField(primary_key=True, db_column='SOC_Id', verbose_name="ID")
    code = models.CharField(max_length=50, unique=True, db_column='SOC_Code', verbose_name="Code")
    intitule = models.CharField(max_length=255, db_column='SOC_Intitule', verbose_name="Intitulé")
    groupe = models.BooleanField(default=False, db_column='SOC_Groupe', verbose_name="Groupe")
    archive = models.BooleanField(null=True, blank=True, db_column='SOC_Archive', verbose_name="Archivé")
    devise = models.ForeignKey('Devise', on_delete=models.SET_NULL, null=True, blank=True, db_column='DEV_Id', verbose_name="Devise")

    class Meta:
        db_table = 'T_E_Societe_SOC'
        verbose_name = "Société"
        verbose_name_plural = "Sociétés"
        ordering = ['code']

    def save(self, *args, **kwargs):
        if not self.id:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT ISNULL(MAX(SOC_Id), 0) + 1 FROM T_E_Societe_SOC")
                self.id = cursor.fetchone()[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.intitule}"


class Stade(models.Model):
    """Modèle pour les stades - équivalent à T_E_Stade_STA"""
    id = models.IntegerField(primary_key=True, db_column='STA_Id', verbose_name="ID")
    intitule = models.CharField(max_length=255, db_column='STA_Intitule', verbose_name="Intitulé")

    class Meta:
        db_table = 'T_E_Stade_STA'
        verbose_name = "Stade"
        verbose_name_plural = "Stades"
        ordering = ['intitule']

    def save(self, *args, **kwargs):
        if not self.id:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT ISNULL(MAX(STA_Id), 0) + 1 FROM T_E_Stade_STA")
                self.id = cursor.fetchone()[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.intitule


class NatureCompte(models.Model):
    """Modèle pour les natures de compte - équivalent à T_E_NatureCompte_NCT"""
    id = models.IntegerField(primary_key=True, db_column='NCT_Id', verbose_name="ID")
    code = models.CharField(max_length=10, unique=True, db_column='NCT_Code', verbose_name="Code")
    intitule = models.CharField(max_length=255, db_column='NCT_Intitule', verbose_name="Intitulé")

    class Meta:
        db_table = 'T_E_NatureCompte_NCT'
        verbose_name = "Nature de Compte"
        verbose_name_plural = "Natures de Compte"
        ordering = ['code']

    def save(self, *args, **kwargs):
        if not self.id:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT ISNULL(MAX(NCT_Id), 0) + 1 FROM T_E_NatureCompte_NCT")
                self.id = cursor.fetchone()[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.intitule}"


class TypeValeur(models.Model):
    """Modèle pour les types de valeur - équivalent à T_E_TypeValeur_TYV"""
    id = models.IntegerField(primary_key=True, db_column='TYV_Id', verbose_name="ID")
    code = models.CharField(max_length=10, unique=True, db_column='TYV_code', verbose_name="Code")
    intitule = models.CharField(max_length=255, db_column='TYV_Intitule', verbose_name="Intitulé")
    commentaires = models.TextField(blank=True, null=True, db_column='TYV_Commentaires', verbose_name="Commentaires")

    class Meta:
        db_table = 'T_E_TypeValeur_TYV'
        verbose_name = "Type de Valeur"
        verbose_name_plural = "Types de Valeur"
        ordering = ['code']

    def save(self, *args, **kwargs):
        if not self.id:
            # Obtenir le prochain ID disponible
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT ISNULL(MAX(TYV_Id), 0) + 1 FROM T_E_TypeValeur_TYV")
                self.id = cursor.fetchone()[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.intitule}"


class PlanCompteGroupe(models.Model):
    """Modèle pour les groupes de plan comptable - équivalent à T_E_PlanCompteGroupe_PLG"""
    id = models.AutoField(primary_key=True, db_column='PLG_Id')
    code = models.CharField(max_length=20, db_column='PLG_Code', verbose_name="Code")
    intitule = models.CharField(max_length=255, db_column='PLG_Intitule', verbose_name="Intitulé")
    nature_compte = models.ForeignKey(NatureCompte, on_delete=models.CASCADE, db_column='NCT_Id', verbose_name="Nature de Compte")
    date_creation = models.DateTimeField(null=True, blank=True, db_column='PLG_DateCreation', verbose_name="Date de création")
    date_maj = models.DateTimeField(null=True, blank=True, db_column='PLG_DateMAJ', verbose_name="Date de modification")

    class Meta:
        db_table = 'T_E_PlanCompteGroupe_PLG'
        verbose_name = "Groupe de Plan Comptable"
        verbose_name_plural = "Groupes de Plan Comptable"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.intitule}"


class PlanCompteLocal(models.Model):
    """Modèle pour les comptes locaux - équivalent à T_E_PlanCompteLocal_PCL"""
    id = models.AutoField(primary_key=True, db_column='PCL_Id')
    compte = models.CharField(max_length=20, db_column='PCL_Compte', verbose_name="Compte")
    intitule = models.CharField(max_length=255, db_column='PCL_Intitule', verbose_name="Intitulé")
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE, db_column='SOC_Id', verbose_name="Société")
    groupe = models.ForeignKey(PlanCompteGroupe, on_delete=models.CASCADE, db_column='PLG_Id', verbose_name="Groupe")
    date_creation = models.DateTimeField(null=True, blank=True, db_column='PLG_DateCreation', verbose_name="Date de création")
    date_maj = models.DateTimeField(null=True, blank=True, db_column='PLG_DateMAJ', verbose_name="Date de modification")

    class Meta:
        db_table = 'T_E_PlanCompteLocal_PCL'
        verbose_name = "Compte Local"
        verbose_name_plural = "Comptes Locaux"
        ordering = ['compte']

    def __str__(self):
        return f"{self.compte} - {self.intitule}"


class Devise(DynamicLabelsMixin, models.Model):
    """Modèle pour les devises - équivalent à T_E_Devises_DEV"""
    id = models.IntegerField(primary_key=True, db_column='DEV_Id', verbose_name="ID")
    code_iso = models.CharField(max_length=3, db_column='DEV_CodeIso', verbose_name="Code ISO", null=True, blank=True)
    intitule = models.CharField(max_length=20, db_column='DEV_Intitule', verbose_name="Intitulé", null=True, blank=True)
    sigle = models.CharField(max_length=3, db_column='DEV_Sigle', verbose_name="Sigle", null=True, blank=True)

    class Meta:
        db_table = 'T_E_Devises_DEV'
        verbose_name = "Devise"
        verbose_name_plural = "Devises"
        ordering = ['code_iso']

    def save(self, *args, **kwargs):
        if not self.id:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT ISNULL(MAX(DEV_Id), 0) + 1 FROM T_E_Devises_DEV")
                self.id = cursor.fetchone()[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code_iso} - {self.intitule}"

# Les libellés dynamiques seront appliqués par l'admin


# Modèles simplifiés pour correspondre à la structure existante de la base
# Les modèles complexes seront ajoutés progressivement selon les besoins