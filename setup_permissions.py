#!/usr/bin/env python
"""
Script pour configurer les permissions et groupes Django
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'port_adhoc_compta.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from comptabilite.models import Societe, Stade, NatureCompte, TypeValeur, PlanCompteGroupe, PlanCompteLocal, Devise

def setup_permissions():
    """Configure les permissions et groupes pour l'application"""
    
    print("🔧 Configuration des permissions et groupes Django...")
    
    # Créer ou récupérer les groupes
    groups = {
        'Gestionnaires': {
            'description': 'Peut gérer toutes les données comptables',
            'permissions': ['add', 'change', 'delete', 'view']
        },
        'Utilisateurs_Standard': {
            'description': 'Peut consulter les données',
            'permissions': ['view']
        },
        'Editeurs': {
            'description': 'Peut consulter et modifier les données',
            'permissions': ['add', 'change', 'view']
        }
    }
    
    # Modèles à configurer
    models = [Societe, Stade, NatureCompte, TypeValeur, PlanCompteGroupe, PlanCompteLocal, Devise]
    
    for group_name, group_config in groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"✅ Groupe '{group_name}' créé")
        else:
            print(f"ℹ️  Groupe '{group_name}' existe déjà")
        
        # Ajouter les permissions au groupe
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            model_name = model._meta.model_name
            
            for perm_codename in group_config['permissions']:
                permission_codename = f"{perm_codename}_{model_name}"
                try:
                    permission = Permission.objects.get(
                        codename=permission_codename,
                        content_type=content_type
                    )
                    group.permissions.add(permission)
                    print(f"   ✅ Permission '{permission_codename}' ajoutée")
                except Permission.DoesNotExist:
                    print(f"   ⚠️  Permission '{permission_codename}' non trouvée")
    
    # Créer ou récupérer l'utilisateur Gilles
    try:
        gilles = User.objects.get(username='Gilles')
        print(f"✅ Utilisateur 'Gilles' trouvé")
    except User.DoesNotExist:
        gilles = User.objects.create_user(
            username='Gilles',
            email='gilles@example.com',
            password='gilles123',
            first_name='Gilles',
            last_name='Coulouarn'
        )
        print(f"✅ Utilisateur 'Gilles' créé")
    
    # Assigner Gilles au groupe des Gestionnaires
    gestionnaires_group = Group.objects.get(name='Gestionnaires')
    gilles.groups.add(gestionnaires_group)
    print(f"✅ Utilisateur 'Gilles' ajouté au groupe 'Gestionnaires'")
    
    # Vérifier les permissions de Gilles
    print(f"\n🔍 Permissions de Gilles:")
    print(f"   - is_staff: {gilles.is_staff}")
    print(f"   - is_superuser: {gilles.is_superuser}")
    print(f"   - Groups: {list(gilles.groups.all())}")
    
    # Tester les permissions spécifiques
    print(f"\n🧪 Test des permissions pour les sociétés:")
    permissions_to_test = [
        'comptabilite.add_societe',
        'comptabilite.change_societe', 
        'comptabilite.delete_societe',
        'comptabilite.view_societe'
    ]
    
    for perm in permissions_to_test:
        has_perm = gilles.has_perm(perm)
        status = "✅" if has_perm else "❌"
        print(f"   {status} {perm}: {has_perm}")
    
    print(f"\n🎉 Configuration terminée !")
    print(f"\n📋 Comptes disponibles:")
    print(f"   - Gilles / gilles123 (Gestionnaire)")
    print(f"   - admin / admin (Super utilisateur)")
    print(f"   - test / test (Utilisateur de test)")

if __name__ == '__main__':
    setup_permissions()
