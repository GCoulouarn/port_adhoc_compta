"""
Context processors pour l'administration Django
"""
from .models import Societe, Devise, PlanCompteLocal, PlanCompteGroupe, NatureCompte, TypeValeur, Stade, Periode


def admin_counts(request):
    """Ajouter les compteurs des modèles dans le contexte de l'admin"""
    if request.path.startswith('/admin/'):
        try:
            return {
                'societe_count': Societe.objects.count(),
                'devise_count': Devise.objects.count(),
                'plancomptelocal_count': PlanCompteLocal.objects.count(),
                'plancomptegroupe_count': PlanCompteGroupe.objects.count(),
                'naturecompte_count': NatureCompte.objects.count(),
                'typevaleur_count': TypeValeur.objects.count(),
                'stade_count': Stade.objects.count(),
                'periode_count': Periode.objects.count(),
            }
        except Exception:
            # En cas d'erreur, retourner des valeurs par défaut
            return {
                'societe_count': 0,
                'devise_count': 0,
                'plancomptelocal_count': 0,
                'plancomptegroupe_count': 0,
                'naturecompte_count': 0,
                'typevaleur_count': 0,
                'stade_count': 0,
                'periode_count': 0,
            }
    return {}
