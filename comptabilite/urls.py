from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuration du routeur pour l'API REST
router = DefaultRouter()
router.register(r'societes', views.SocieteViewSet)
router.register(r'stades', views.StadeViewSet)
router.register(r'natures-compte', views.NatureCompteViewSet)
router.register(r'types-valeur', views.TypeValeurViewSet)
router.register(r'groupes-compte', views.PlanCompteGroupeViewSet)
router.register(r'comptes-locaux', views.PlanCompteLocalViewSet)
router.register(r'devises', views.DeviseViewSet)
# router.register(r'tiers', views.TiersViewSet)
# router.register(r'versions', views.VersionViewSet)
# router.register(r'ecritures', views.FinanceFaitsViewSet)

app_name = 'comptabilite'

urlpatterns = [
    # Pages web
    path('', views.index, name='index'),
    path('societes/', views.SocieteListView.as_view(), name='societe_list'),
    path('societes/<int:pk>/', views.SocieteDetailView.as_view(), name='societe_detail'),
    path('societes/create/', views.SocieteCreateView.as_view(), name='societe_create'),
    path('societes/<int:pk>/edit/', views.SocieteUpdateView.as_view(), name='societe_edit'),
    path('societes/<int:pk>/delete/', views.SocieteDeleteView.as_view(), name='societe_delete'),
    path('devises/', views.DeviseListView.as_view(), name='devise_list'),
    path('devises/<int:pk>/', views.DeviseDetailView.as_view(), name='devise_detail'),
    path('devises/create/', views.DeviseCreateView.as_view(), name='devise_create'),
    path('devises/<int:pk>/edit/', views.DeviseUpdateView.as_view(), name='devise_edit'),
    path('devises/<int:pk>/delete/', views.DeviseDeleteView.as_view(), name='devise_delete'),
    
    # Authentification utilisateur
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    
    # path('ecritures/', views.FinanceFaitsListView.as_view(), name='finance_faits_list'),
    
    # API REST
    path('api/', include(router.urls)),
]
