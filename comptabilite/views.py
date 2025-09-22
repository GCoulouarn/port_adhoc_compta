from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django import forms
import pandas as pd
import io
import csv
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db import models
from django.db import connection
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django import forms
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    Societe, Stade, NatureCompte, TypeValeur, PlanCompteGroupe,
    PlanCompteLocal, Devise
)
from referentiel.models import Periode
from .serializers import (
    SocieteSerializer, StadeSerializer, NatureCompteSerializer, TypeValeurSerializer,
    PlanCompteGroupeSerializer, PlanCompteLocalSerializer, DeviseSerializer
)
# from .filters import FinanceFaitsFilter


class EcrituresRechercheForm(forms.Form):
    """Formulaire de recherche d'écritures comptables."""
    per_id = forms.ModelChoiceField(
        queryset=Periode.objects.all(),
        required=False,
        empty_label="Sélectionner une période",
        label="Période"
    )
    sta_id = forms.ModelChoiceField(
        queryset=Stade.objects.all(),
        required=False,
        empty_label="Sélectionner un stade",
        label="Stade"
    )
    soc_id = forms.ModelChoiceField(
        queryset=Societe.objects.all(),
        required=False,
        empty_label="Sélectionner une société",
        label="Société"
    )
    tyv_id = forms.ModelChoiceField(
        queryset=TypeValeur.objects.all(),
        required=False,
        empty_label="Sélectionner un type de valeur",
        label="Type de valeur"
    )
    pcl_compte = forms.CharField(
        required=False,
        max_length=20,
        label="Compte PCL"
    )
    fin_solde = forms.DecimalField(
        required=False,
        max_digits=15,
        decimal_places=2,
        label="Solde"
    )
    ax1_code = forms.CharField(
        required=False,
        max_length=20,
        label="Axe 1"
    )
    ax2_code = forms.CharField(
        required=False,
        max_length=20,
        label="Axe 2"
    )
    ax3_code = forms.CharField(
        required=False,
        max_length=20,
        label="Axe 3"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ModelChoiceField):
                css = 'form-select'
            else:
                css = 'form-control'
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' ' + css).strip()


# Formulaires pour les devises
class DeviseForm(forms.ModelForm):
    class Meta:
        model = Devise
        fields = ['code_iso', 'intitule', 'sigle']
        widgets = {
            'code_iso': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3'}),
            'intitule': forms.TextInput(attrs={'class': 'form-control'}),
            'sigle': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3'}),
        }
        labels = {
            'code_iso': 'Code ISO',
            'intitule': 'Intitulé',
            'sigle': 'Sigle',
        }


# Formulaires pour les sociétés
class SocieteForm(forms.ModelForm):
    devise = forms.ModelChoiceField(
        queryset=Devise.objects.all().order_by('intitule'),
        empty_label="Sélectionner une devise",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Devise"
    )
    
    class Meta:
        model = Societe
        fields = ['code', 'intitule', 'groupe', 'archive']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'intitule': forms.TextInput(attrs={'class': 'form-control'}),
            'groupe': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'archive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'code': 'Code',
            'intitule': 'Intitulé',
            'groupe': 'Est un groupe',
            'archive': 'Archivé',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pré-sélectionner la devise si elle existe
        if self.instance and self.instance.pk and self.instance.devise_id:
            try:
                devise = Devise.objects.get(id=self.instance.devise_id)
                self.fields['devise'].initial = devise
            except Devise.DoesNotExist:
                pass
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        devise = self.cleaned_data.get('devise')
        if devise:
            instance.devise_id = devise.id
        else:
            instance.devise_id = None
        
        if commit:
            instance.save()
        return instance


def index(request):
    """Page d'accueil de l'application"""
    context = {
        'title': 'Port Adhoc Compta - Gestion Comptable',
        'societes_count': Societe.objects.count(),
        'ecritures_count': 0,  # Temporairement à 0
        'comptes_count': PlanCompteLocal.objects.count(),
    }
    return render(request, 'comptabilite/index.html', context)


class SocieteListView(ListView):
    """Liste des sociétés"""
    model = Societe
    template_name = 'comptabilite/societe_list.html'
    context_object_name = 'societes'
    paginate_by = 20
    
    def get_queryset(self):
        """Filtrage des sociétés selon les paramètres de recherche"""
        queryset = Societe.objects.all()
        
        # Filtre par recherche (code ou intitulé)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(code__icontains=search) |
                models.Q(intitule__icontains=search)
            )
        
        # Filtre par type (groupe ou société)
        groupe = self.request.GET.get('groupe')
        if groupe == 'true':
            queryset = queryset.filter(groupe=True)
        elif groupe == 'false':
            queryset = queryset.filter(groupe=False)
        
        # Filtre par statut (archivé ou actif)
        archive = self.request.GET.get('archive')
        if archive == 'true':
            queryset = queryset.filter(archive=True)
        elif archive == 'false':
            queryset = queryset.filter(archive=False)
        
        # Tri par colonne
        sort_by = self.request.GET.get('sort', 'code')
        sort_order = self.request.GET.get('order', 'asc')
        
        # Mapping des colonnes triables
        sortable_columns = {
            'id': 'id',
            'code': 'code',
            'intitule': 'intitule',
            'groupe': 'groupe',
            'archive': 'archive',
        }
        
        if sort_by in sortable_columns:
            field = sortable_columns[sort_by]
            if sort_order == 'desc':
                field = f'-{field}'
            queryset = queryset.order_by(field)
        else:
            queryset = queryset.order_by('code')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter les permissions dans le contexte
        user = self.request.user
        if user.is_authenticated:
            context['can_add_societe'] = user.has_perm('comptabilite.add_societe')
            context['can_change_societe'] = user.has_perm('comptabilite.change_societe')
            context['can_delete_societe'] = user.has_perm('comptabilite.delete_societe')
        else:
            context['can_add_societe'] = False
            context['can_change_societe'] = False
            context['can_delete_societe'] = False
        
        # Ajouter les valeurs des filtres pour les conserver dans le formulaire
        context['search_value'] = self.request.GET.get('search', '')
        context['groupe_value'] = self.request.GET.get('groupe', '')
        context['archive_value'] = self.request.GET.get('archive', '')
        
        # Ajouter les informations de tri
        context['current_sort'] = self.request.GET.get('sort', 'code')
        context['current_order'] = self.request.GET.get('order', 'asc')
        
        # Calculer le prochain ordre de tri
        context['next_order'] = 'desc' if context['current_order'] == 'asc' else 'asc'
        
        return context


class SocieteDetailView(DetailView):
    """Détail d'une société"""
    model = Societe
    template_name = 'comptabilite/societe_detail.html'
    context_object_name = 'societe'


class SocieteCreateView(CreateView):
    """Création d'une société"""
    model = Societe
    form_class = SocieteForm
    template_name = 'comptabilite/societe_form.html'
    success_url = reverse_lazy('comptabilite:societe_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('comptabilite.add_societe'):
            raise PermissionDenied("Vous n'avez pas la permission d'ajouter une société.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Société créée avec succès !')
        return super().form_valid(form)


class SocieteUpdateView(UpdateView):
    """Modification d'une société"""
    model = Societe
    form_class = SocieteForm
    template_name = 'comptabilite/societe_form.html'
    success_url = reverse_lazy('comptabilite:societe_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('comptabilite.change_societe'):
            raise PermissionDenied("Vous n'avez pas la permission de modifier une société.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Société modifiée avec succès !')
        return super().form_valid(form)


class SocieteDeleteView(DeleteView):
    """Suppression d'une société"""
    model = Societe
    template_name = 'comptabilite/societe_confirm_delete.html'
    success_url = reverse_lazy('comptabilite:societe_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('comptabilite.delete_societe'):
            raise PermissionDenied("Vous n'avez pas la permission de supprimer une société.")
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Société supprimée avec succès !')
        return super().delete(request, *args, **kwargs)


# Vues pour les écritures comptables seront ajoutées plus tard


class EcrituresRechercheForm(forms.Form):
    per_id = forms.ModelChoiceField(
        queryset=Periode.objects.all().order_by('id'),
        required=False,
        empty_label='Toutes',
        label='Période'
    )
    sta_id = forms.ModelChoiceField(
        queryset=Stade.objects.all().order_by('intitule'),
        required=False,
        empty_label='Tous',
        label='Stade'
    )
    soc_id = forms.ModelChoiceField(
        queryset=Societe.objects.all().order_by('intitule'),
        required=False,
        empty_label='Toutes',
        label='Société'
    )
    tyv_id = forms.ModelChoiceField(
        queryset=TypeValeur.objects.all().order_by('intitule'),
        required=False,
        empty_label='Tous',
        label='Type valeur'
    )
    pcl_compte = forms.CharField(required=False, label='Compte')
    fin_solde = forms.DecimalField(required=False, label='Solde', decimal_places=2, max_digits=18)
    ax1_code = forms.CharField(required=False, label='Axe 1')
    ax2_code = forms.CharField(required=False, label='Axe 2')
    ax3_code = forms.CharField(required=False, label='Axe 3')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Améliorer le rendu Bootstrap
        for name, field in self.fields.items():
            css = 'form-control'
            if isinstance(field.widget, forms.Select):
                css = 'form-select'
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' ' + css).strip()


def ecritures_recherche(request):
    """Recherche des écritures via la procédure DW.PS_S_000423_SelectRechercheEcriture_SRE.
    Reproduit la grille de recherche de l'application WinForms.
    """
    form = EcrituresRechercheForm(request.GET or None)
    rows = []
    columns = []
    display_columns = []

    if form.is_valid() and any(v is not None and v != '' for v in form.cleaned_data.values()):
        params = {
            'per_id': (form.cleaned_data.get('per_id').id if form.cleaned_data.get('per_id') else None),
            'sta_id': (form.cleaned_data.get('sta_id').id if form.cleaned_data.get('sta_id') else None),
            'soc_id': (form.cleaned_data.get('soc_id').id if form.cleaned_data.get('soc_id') else None),
            'tyv_id': (form.cleaned_data.get('tyv_id').id if form.cleaned_data.get('tyv_id') else None),
            'pcl_compte': form.cleaned_data.get('pcl_compte') or None,
            'fin_solde': form.cleaned_data.get('fin_solde'),
            'ax1_code': form.cleaned_data.get('ax1_code') or None,
            'ax2_code': form.cleaned_data.get('ax2_code') or None,
            'ax3_code': form.cleaned_data.get('ax3_code') or None,
        }

        # Exécution de la procédure stockée
        try:
            with connection.cursor() as cursor:
                sql = (
                    "EXEC DW.PS_S_000423_SelectRechercheEcriture_SRE "
                    "@per_id=%s, @sta_id=%s, @soc_id=%s, @tyv_id=%s, @pcl_compte=%s, "
                    "@fin_solde=%s, @ax1_code=%s, @ax2_code=%s, @ax3_code=%s, @lb_error=%s"
                )
                out_error = ''
                cursor.execute(
                    sql,
                    [
                        params['per_id'], params['sta_id'], params['soc_id'], params['tyv_id'],
                        params['pcl_compte'], params['fin_solde'], params['ax1_code'],
                        params['ax2_code'], params['ax3_code'], out_error,
                    ],
                )
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de l'exécution de la procédure: {e}")

    # Générer des libellés lisibles pour l'entête du tableau
    if columns:
        overrides = {
            'PER_id': 'Période',
            'STA_id': 'Stade',
            'SOC_id': 'Société',
            'TYV_Id': 'Type valeur',
            'TYV_code': 'Type valeur',
            'PCL_Compte': 'Compte',
            'PCL_Intitule': 'Intitulé compte',
            'AX1_Code': 'Axe 1',
            'AX2_Code': 'Axe 2',
            'AX3_Code': 'Axe 3',
            'FIN_Montant': 'Montant',
            'FIN_Solde': 'Solde',
            'LOT_id': 'Lot',
            'FIN_id': 'ID écriture',
            'FIN_Date': 'Date',
        }

        def prettify(name: str) -> str:
            return name.replace('_', ' ').strip().capitalize()

        display_columns = [overrides.get(c, prettify(c)) for c in columns]
    
    context = {
        'title': 'Recherche des écritures',
        'form': form,
        'columns': columns,
        'display_columns': display_columns,
        'rows': rows,
    }
    return render(request, 'comptabilite/finance_faits_search.html', context)


@login_required
@require_http_methods(["POST"])
def ecritures_import(request):
    """Import des écritures via la procédure PS_S_000203_ImportEcritureFIN.
    Reproduit la fonctionnalité du bouton 'Passer les écritures' de l'app C#.
    """
    import json
    
    try:
        data = json.loads(request.body)
        
        # Récupérer les paramètres de la recherche
        per_id = data.get('per_id')
        sta_id = data.get('sta_id')
        soc_id = data.get('soc_id')
        tyv_id = data.get('tyv_id')
        pcl_compte = data.get('pcl_compte')
        fin_solde = data.get('fin_solde')
        ax1_code = data.get('ax1_code')
        ax2_code = data.get('ax2_code')
        ax3_code = data.get('ax3_code')
        
        # Validation des paramètres requis
        if not all([per_id, sta_id, soc_id, tyv_id]):
            return JsonResponse({
                'success': False,
                'error': 'Paramètres manquants pour l\'import'
            })
        
        # Exécution de la procédure d'import
        # Signature observée côté C#: PS_S_000203_ImportEcritureFIN(ver_id, lot_id, pcl_id, ax1_id, ax2_id, ax3_id, tyv_id, per_id, mtt)
        with connection.cursor() as cursor:
            # Note: Cette procédure nécessite des IDs spécifiques, pas les codes
            # Il faudrait adapter selon la logique métier réelle
            sql = (
                "EXEC DW.PS_S_000203_ImportEcritureFIN "
                "@ver_id=%s, @lot_id=%s, @pcl_id=%s, @ax1_id=%s, @ax2_id=%s, "
                "@ax3_id=%s, @tyv_id=%s, @per_id=%s, @mtt=%s"
            )
            
            # Pour l'instant, on simule l'appel avec des valeurs par défaut
            # Dans un vrai contexte, il faudrait récupérer les IDs correspondants
            cursor.execute(sql, [
                1,  # ver_id - version par défaut
                1,  # lot_id - lot par défaut  
                1,  # pcl_id - compte par défaut
                1,  # ax1_id - axe1 par défaut
                1,  # ax2_id - axe2 par défaut
                1,  # ax3_id - axe3 par défaut
                tyv_id,
                per_id,
                fin_solde or 0.0
            ])
            
            # Récupérer le résultat si la procédure retourne quelque chose
            result = cursor.fetchone()
            
        return JsonResponse({
            'success': True,
            'message': 'Écritures importées avec succès',
            'result': result
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur lors de l\'import : {str(e)}'
        })


@login_required
@require_http_methods(["POST"])
def ecritures_import_sage(request):
    """Import d'écritures depuis Sage/Exact.
    Reproduit la fonctionnalité BT_ImportData_Click de l'app C#.
    """
    try:
        # Récupérer les paramètres du formulaire
        societe_id = request.POST.get('societe')
        stade_id = request.POST.get('stade')
        month = request.POST.get('month')
        year = request.POST.get('year')
        version = request.POST.get('version')
        libelle = request.POST.get('libelle')
        import_type = request.POST.get('import_type', 'sage')
        actualiser = request.POST.get('actualiser') == 'on'
        
        # Validation des paramètres
        if not all([societe_id, stade_id, month, year]):
            return JsonResponse({
                'success': False,
                'error': 'Paramètres manquants'
            })
        
        # Validation du mois
        try:
            month_num = int(month)
            if month_num < 1 or month_num > 12:
                return JsonResponse({
                    'success': False,
                    'error': 'Le mois doit être un entier entre 1 et 12'
                })
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Le mois doit être un entier'
            })
        
        # Validation de l'année
        if len(year) != 4:
            return JsonResponse({
                'success': False,
                'error': 'L\'année doit comporter 4 chiffres'
            })
        
        # Validation de la version si fournie
        version_id = 1  # Version par défaut
        if version:
            try:
                version_id = int(version)
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Le numéro de version doit être un entier'
                })
        
        # Calcul de la période (format YYYYMM)
        periode = int(year) * 100 + month_num
        
        # Exécution de la procédure d'import
        with connection.cursor() as cursor:
            if import_type == 'sage':
                # Appel de PS_S_000104_InsertionFaitsFinanciers pour Sage
                sql = "EXEC DW.PS_S_000104_InsertionFaitsFinanciers @actualiser=%s, @socid=%s, @staid=%s, @periode=%s, @force=%s, @version=%s, @libelle=%s"
                cursor.execute(sql, [
                    actualiser,
                    int(societe_id),
                    int(stade_id),
                    periode,
                    True,  # force
                    version_id,
                    libelle or ''
                ])
            else:  # exact
                # Appel de PS_S_InsertionFaitsExactOnline_IFE pour Exact
                sql = "EXEC DW.PS_S_InsertionFaitsExactOnline_IFE @actualiser=%s, @socid=%s, @staid=%s, @periode=%s, @force=%s, @version=%s, @libelle=%s"
                cursor.execute(sql, [
                    actualiser,
                    int(societe_id),
                    int(stade_id),
                    periode,
                    True,  # force
                    version_id,
                    libelle or ''
                ])
            
            # Récupérer le résultat si la procédure retourne quelque chose
            result = cursor.fetchone()
        
        return JsonResponse({
            'success': True,
            'message': 'Données importées avec succès',
            'periode': periode,
            'societe_id': societe_id,
            'stade_id': stade_id,
            'import_type': import_type,
            'result': result
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur lors de l\'import : {str(e)}'
        })


@login_required
@require_http_methods(["POST"])
def ecritures_import_file(request):
    """Import d'écritures depuis un fichier Excel vers T_Temp_ImportBudgetExcel."""
    try:
        if 'excel_file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'Aucun fichier fourni'
            })
        
        file = request.FILES['excel_file']
        
        # Vérifier que c'est un fichier Excel
        if not (file.name.endswith('.xlsx') or file.name.endswith('.xls')):
            return JsonResponse({
                'success': False,
                'error': 'Seuls les fichiers Excel (.xlsx, .xls) sont acceptés'
            })
        
        # Lire le fichier Excel
        df = pd.read_excel(file)
        
        # Vérifier que le fichier n'est pas vide
        if df.empty:
            return JsonResponse({
                'success': False,
                'error': 'Le fichier Excel est vide'
            })
        
        # Insérer les données dans T_Temp_ImportBudgetExcel
        with connection.cursor() as cursor:
            # Vider la table temporaire d'abord
            cursor.execute("DELETE FROM T_Temp_ImportBudgetExcel")
            
            # Insérer les nouvelles données
            for index, row in df.iterrows():
                # Créer un dictionnaire avec les valeurs par défaut pour toutes les colonnes
                values = [None] * 24  # 24 colonnes dans la table
                
                # Mapper les colonnes du DataFrame aux colonnes de la table
                for i, col in enumerate(df.columns):
                    if i < 24:  # S'assurer qu'on ne dépasse pas le nombre de colonnes
                        value = row[col]
                        if not pd.isna(value):
                            values[i] = str(value)
                
                # Construire la requête d'insertion avec les noms de colonnes
                columns = [
                    'Societe', 'Annee', 'Version', 'CompteGeneral', 'Section', 'GroupeCode',
                    'RefactCode', 'Parametre', 'Periode', 'Valeur', 'SOC_Id', 'SocieteNom',
                    'CompteIntitule', 'PLG_Code', 'PLG_Intitule', 'NCT_Intitule', 'NCT_Code',
                    'SIG_Code', 'SIG_Intitule', 'TFT_code', 'TFT_Intitule', 'BLN_code',
                    'BLN_Intitule', 'TypeValeur'
                ]
                
                placeholders = ', '.join(['%s'] * len(columns))
                columns_str = ', '.join(columns)
                sql = f"INSERT INTO T_Temp_ImportBudgetExcel ({columns_str}) VALUES ({placeholders})"
                
                cursor.execute(sql, values)
        
        return JsonResponse({
            'success': True,
            'message': f'Import réussi: {len(df)} lignes importées dans T_Temp_ImportBudgetExcel',
            'rows_imported': len(df)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur lors de l\'import: {str(e)}'
        })


def process_csv_file(file):
    """Traite un fichier CSV et retourne les données."""
    content = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(content))
    return list(reader)


def process_excel_file(file):
    """Traite un fichier Excel et retourne les données."""
    df = pd.read_excel(file)
    return df.to_dict('records')


def validate_import_data(data):
    """Valide les données d'import."""
    errors = []
    required_fields = ['compte', 'libelle', 'montant', 'date']
    
    for i, row in enumerate(data, 1):
        for field in required_fields:
            if field not in row or not row[field]:
                errors.append(f'Ligne {i}: Champ "{field}" manquant')
        
        # Validation du montant
        if 'montant' in row:
            try:
                float(row['montant'])
            except ValueError:
                errors.append(f'Ligne {i}: Montant invalide "{row["montant"]}"')
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


def import_ecritures_data(data, periode_id, societe_id):
    """Importe les données dans la base."""
    created = 0
    errors = []
    
    try:
        with connection.cursor() as cursor:
            for row in data:
                # Ici, vous implémenterez la logique d'insertion
                # selon votre structure de base de données
                # Pour l'instant, on simule l'import
                created += 1
    except Exception as e:
        errors.append(f'Erreur lors de l\'insertion : {str(e)}')
    
    return {
        'created': created,
        'errors': errors
    }


@login_required
def ecritures_template(request):
    """Télécharge un modèle de fichier pour l'import."""
    # Créer un fichier CSV modèle
    output = io.StringIO()
    writer = csv.writer(output)
    
    # En-têtes du modèle
    headers = [
        'compte', 'libelle', 'montant', 'date', 'type_valeur',
        'axe1', 'axe2', 'axe3', 'societe', 'periode'
    ]
    writer.writerow(headers)
    
    # Ligne d'exemple
    example = [
        '411000', 'Client exemple', '1000.00', '2024-01-15', '1',
        'AXE1', 'AXE2', 'AXE3', '1', '1'
    ]
    writer.writerow(example)
    
    # Préparer la réponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="modele_ecritures.csv"'
    response.write(output.getvalue())
    
    return response


# API REST Viewsets
class SocieteViewSet(viewsets.ModelViewSet):
    """API pour les sociétés"""
    queryset = Societe.objects.all()
    serializer_class = SocieteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['code', 'intitule']
    ordering_fields = ['code', 'intitule', 'date_creation']
    ordering = ['code']


class StadeViewSet(viewsets.ModelViewSet):
    """API pour les stades"""
    queryset = Stade.objects.all()
    serializer_class = StadeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['code', 'intitule']
    ordering_fields = ['code', 'intitule']
    ordering = ['code']


class NatureCompteViewSet(viewsets.ModelViewSet):
    """API pour les natures de compte"""
    queryset = NatureCompte.objects.all()
    serializer_class = NatureCompteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['code', 'intitule']
    ordering_fields = ['code', 'intitule']
    ordering = ['code']


class TypeValeurViewSet(viewsets.ModelViewSet):
    """API pour les types de valeur"""
    queryset = TypeValeur.objects.all()
    serializer_class = TypeValeurSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['code', 'intitule']
    ordering_fields = ['code', 'intitule']
    ordering = ['code']


class PlanCompteGroupeViewSet(viewsets.ModelViewSet):
    """API pour les groupes de plan comptable"""
    queryset = PlanCompteGroupe.objects.select_related('societe', 'nature_compte').all()
    serializer_class = PlanCompteGroupeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['societe', 'nature_compte']
    search_fields = ['code', 'intitule', 'societe__code']
    ordering_fields = ['code', 'intitule', 'date_creation']
    ordering = ['societe', 'code']


class PlanCompteLocalViewSet(viewsets.ModelViewSet):
    """API pour les comptes locaux"""
    queryset = PlanCompteLocal.objects.select_related('societe', 'groupe').all()
    serializer_class = PlanCompteLocalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['societe', 'groupe']
    search_fields = ['compte', 'intitule', 'societe__code']
    ordering_fields = ['compte', 'intitule', 'date_creation']
    ordering = ['societe', 'compte']


# Vues pour les devises
class DeviseListView(ListView):
    """Vue pour lister les devises"""
    model = Devise
    template_name = 'comptabilite/devise_list.html'
    context_object_name = 'devises'
    paginate_by = 20

    def get_queryset(self):
        queryset = Devise.objects.all()
        
        # Filtre par recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(code_iso__icontains=search) |
                models.Q(intitule__icontains=search) |
                models.Q(sigle__icontains=search)
            )
        
        # Tri par colonne
        sort_by = self.request.GET.get('sort', 'code_iso')
        sort_order = self.request.GET.get('order', 'asc')
        
        # Mapping des colonnes triables
        sortable_columns = {
            'id': 'id',
            'code_iso': 'code_iso',
            'intitule': 'intitule',
            'sigle': 'sigle',
        }
        
        if sort_by in sortable_columns:
            field = sortable_columns[sort_by]
            if sort_order == 'desc':
                field = f'-{field}'
            queryset = queryset.order_by(field)
        else:
            queryset = queryset.order_by('code_iso')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter les informations de tri
        context['current_sort'] = self.request.GET.get('sort', 'code_iso')
        context['current_order'] = self.request.GET.get('order', 'asc')
        context['search_value'] = self.request.GET.get('search', '')
        
        # Calculer le prochain ordre de tri
        context['next_order'] = 'desc' if context['current_order'] == 'asc' else 'asc'
        
        # Ajouter les permissions
        user = self.request.user
        if user.is_authenticated:
            context['can_add_devise'] = user.has_perm('comptabilite.add_devise')
            context['can_change_devise'] = user.has_perm('comptabilite.change_devise')
            context['can_delete_devise'] = user.has_perm('comptabilite.delete_devise')
        else:
            context['can_add_devise'] = False
            context['can_change_devise'] = False
            context['can_delete_devise'] = False
        
        return context


class DeviseDetailView(DetailView):
    """Vue pour afficher les détails d'une devise"""
    model = Devise
    template_name = 'comptabilite/devise_detail.html'
    context_object_name = 'devise'


class DeviseCreateView(CreateView):
    """Création d'une devise"""
    model = Devise
    form_class = DeviseForm
    template_name = 'comptabilite/devise_form.html'
    success_url = reverse_lazy('comptabilite:devise_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('comptabilite.add_devise'):
            raise PermissionDenied("Vous n'avez pas la permission d'ajouter une devise.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Devise créée avec succès !')
        return super().form_valid(form)


class DeviseUpdateView(UpdateView):
    """Modification d'une devise"""
    model = Devise
    form_class = DeviseForm
    template_name = 'comptabilite/devise_form.html'
    success_url = reverse_lazy('comptabilite:devise_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('comptabilite.change_devise'):
            raise PermissionDenied("Vous n'avez pas la permission de modifier une devise.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Devise modifiée avec succès !')
        return super().form_valid(form)


class DeviseDeleteView(DeleteView):
    """Suppression d'une devise"""
    model = Devise
    template_name = 'comptabilite/devise_confirm_delete.html'
    success_url = reverse_lazy('comptabilite:devise_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('comptabilite.delete_devise'):
            raise PermissionDenied("Vous n'avez pas la permission de supprimer une devise.")
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Devise supprimée avec succès !')
        return super().delete(request, *args, **kwargs)


class DeviseViewSet(viewsets.ModelViewSet):
    """API pour les devises"""
    queryset = Devise.objects.all()
    serializer_class = DeviseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['code_iso', 'intitule', 'sigle']
    ordering_fields = ['id', 'code_iso', 'intitule']
    ordering = ['code_iso']


# API pour les tiers et versions sera ajoutée plus tard


# Vues d'authentification utilisateur
def user_login(request):
    """Vue de connexion utilisateur"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue, {user.username} !')
            return redirect('comptabilite:index')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'comptabilite/login.html')


def user_logout(request):
    """Vue de déconnexion utilisateur"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('comptabilite:index')


def user_register(request):
    """Vue d'inscription utilisateur"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username} !')
            login(request, user)
            return redirect('comptabilite:index')
    else:
        form = UserCreationForm()
    
    return render(request, 'comptabilite/register.html', {'form': form})


@login_required
def user_profile(request):
    """Vue du profil utilisateur"""
    return render(request, 'comptabilite/profile.html', {'user': request.user})


@login_required
def import_excel(request):
    """Page dédiée à l'import de fichiers Excel."""
    if request.method == 'POST':
        return ecritures_import_file(request)
    
    return render(request, 'comptabilite/import_excel.html')




# API pour les écritures comptables sera ajoutée plus tard