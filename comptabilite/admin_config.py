"""
Configuration de l'administration Django pour organiser les modèles par sections
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path, include
from django.shortcuts import render
from django.utils.html import format_html
from .models import Periode


class ReferentielAdminSite(AdminSite):
    """Site d'administration personnalisé pour la section Référentiel"""
    site_header = "Référentiel - Port Adhoc Compta"
    site_title = "Référentiel"
    index_title = "Gestion des Référentiels"
    
    def index(self, request, extra_context=None):
        """Page d'accueil personnalisée pour la section Référentiel"""
        context = {
            'title': 'Référentiel',
            'subtitle': 'Gestion des données de référence',
            'models': [
                {
                    'name': 'Périodes',
                    'description': 'Gestion des périodes comptables',
                    'url': 'periode/',
                    'count': Periode.objects.count(),
                }
            ]
        }
        return render(request, 'admin/referentiel_index.html', context)


# Créer une instance du site d'administration personnalisé
referentiel_admin = ReferentielAdminSite(name='referentiel')

# Configuration des modèles pour la section Référentiel
from .admin import PeriodeAdmin
referentiel_admin.register(Periode, PeriodeAdmin)
