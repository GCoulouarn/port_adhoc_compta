from django.contrib import admin
from .models import (
    Societe, Stade, NatureCompte, TypeValeur, PlanCompteGroupe,
    PlanCompteLocal, Devise
)


@admin.register(Societe)
class SocieteAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'intitule', 'groupe', 'archive']
    list_filter = ['groupe', 'archive']
    search_fields = ['code', 'intitule']
    ordering = ['id']
    list_display_links = ['id', 'code']


@admin.register(Stade)
class StadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'intitule']
    search_fields = ['intitule']
    ordering = ['id']
    list_display_links = ['id', 'intitule']


@admin.register(NatureCompte)
class NatureCompteAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'intitule']
    search_fields = ['code', 'intitule']
    ordering = ['id']
    list_display_links = ['id', 'code']


@admin.register(TypeValeur)
class TypeValeurAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'intitule', 'commentaires']
    search_fields = ['code', 'intitule']
    ordering = ['id']
    list_display_links = ['id', 'code']
    list_editable = ['commentaires']


@admin.register(PlanCompteGroupe)
class PlanCompteGroupeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'intitule', 'nature_compte']
    list_filter = ['nature_compte']
    search_fields = ['code', 'intitule']
    ordering = ['id']
    list_display_links = ['id', 'code']


@admin.register(PlanCompteLocal)
class PlanCompteLocalAdmin(admin.ModelAdmin):
    list_display = ['id', 'compte', 'intitule', 'societe', 'groupe']
    list_filter = ['societe', 'groupe']
    search_fields = ['compte', 'intitule', 'societe__code']
    ordering = ['id']
    list_display_links = ['id', 'compte']


@admin.register(Devise)
class DeviseAdmin(admin.ModelAdmin):
    list_display = ['id', 'code_iso', 'intitule', 'sigle']
    search_fields = ['code_iso', 'intitule', 'sigle']
    ordering = ['id']
    list_display_links = ['id', 'code_iso']
    list_editable = ['intitule', 'sigle']