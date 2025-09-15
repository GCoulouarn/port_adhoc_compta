from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db import models
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
    PlanCompteLocal, Devise, Periode
)
from .serializers import (
    SocieteSerializer, StadeSerializer, NatureCompteSerializer, TypeValeurSerializer,
    PlanCompteGroupeSerializer, PlanCompteLocalSerializer, DeviseSerializer, PeriodeSerializer
)
# from .filters import FinanceFaitsFilter


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


# =============================================================================
# SECTION RÉFÉRENTIEL
# =============================================================================

class PeriodeViewSet(viewsets.ModelViewSet):
    """API pour les périodes"""
    queryset = Periode.objects.all()
    serializer_class = PeriodeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['annee', 'mois', 'trimestre_civil']
    search_fields = ['annee', 'mois']
    ordering_fields = ['id', 'annee', 'mois', 'date']
    ordering = ['annee', 'mois']


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


# API pour les écritures comptables sera ajoutée plus tard