# 📝 Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.0.0] - 2025-09-15

### ✨ Ajouté
- **Système de libellés dynamiques** : Gestion centralisée des libellés via la table `AdminText`
- **Application `parametres`** : Nouvelle application dédiée à la gestion des paramètres
- **Middleware `AdminLabelMiddleware`** : Application automatique des libellés dynamiques
- **Context processor `admin_labels`** : Injection des libellés dans tous les templates
- **Champ `display_order`** : Contrôle de l'ordre d'affichage des modèles par section
- **Relation Devise-Société** : ForeignKey entre `Societe` et `Devise`
- **Admin personnalisé des sociétés** : Affichage de la devise, filtres et recherche
- **Templates personnalisés** : `base_site.html`, `app_list.html`, `index.html`
- **Script JavaScript de tri** : Réorganisation automatique des modèles selon l'ordre défini
- **Support multilingue** : Français et anglais avec fallback
- **Interface d'administration personnalisable** : Tous les libellés modifiables
- **Sections dynamiques** : "Comptabilité" → "Finance Consolidation"
- **Ordre d'affichage configurable** : Contrôle total de l'ordre des modèles
- **Filtres et recherche avancés** : Par devise, groupe, statut
- **Formulaires organisés** : Champs groupés par catégorie
- **Masquage du sélecteur de langue** : Interface épurée
- **Cache des libellés** : Optimisation des performances
- **Migration de la base de données** : Support de la relation devise-société
- **Documentation complète** : Guide d'utilisation et d'installation

### 🔧 Modifié
- **Modèle `Societe`** : Ajout du champ `devise` avec ForeignKey
- **Admin des sociétés** : Enrichissement avec affichage de la devise
- **Templates admin** : Personnalisation complète de l'interface
- **Settings.py** : Ajout du middleware et context processor
- **Structure de la base de données** : Ajout de la colonne `ADT_DisplayOrder`

### 🐛 Corrigé
- **Problèmes de performance** : Optimisation des requêtes de libellés
- **Gestion des langues** : Fallback français en cas de langue non trouvée
- **Affichage des libellés** : Correction des clés avec majuscules/minuscules
- **Tri des modèles** : Implémentation JavaScript pour l'ordre d'affichage

### 🔒 Sécurité
- **Validation des données** : Contrôle des entrées utilisateur
- **Protection CSRF** : Tokens CSRF activés
- **Authentification** : Système Django standard
- **Autorisation** : Permissions par modèle

### 📚 Documentation
- **README.md** : Guide de démarrage rapide
- **DOCUMENTATION.md** : Documentation technique complète
- **CHANGELOG.md** : Historique des modifications
- **Commentaires de code** : Documentation inline

### 🚀 Performance
- **Cache des libellés** : Évite les requêtes répétées
- **Middleware optimisé** : Exécution uniquement sur les requêtes admin
- **Requêtes groupées** : Récupération de tous les libellés en une fois
- **Templates optimisés** : Chargement efficace des ressources

### 🧪 Tests
- **Tests unitaires** : Couverture des fonctionnalités principales
- **Tests d'intégration** : Vérification du système de libellés
- **Tests de performance** : Validation des optimisations

### 📦 Dépendances
- **Django 5.0.6** : Framework web principal
- **pyodbc 5.0.1** : Connexion SQL Server
- **django-cors-headers 4.3.1** : Gestion CORS
- **python-decouple 3.8** : Gestion des variables d'environnement

## [0.1.0] - 2025-09-01

### ✨ Ajouté
- **Structure de base** : Projet Django initial
- **Modèles comptables** : Societe, Devise, NatureCompte, etc.
- **Interface d'administration** : Admin Django standard
- **Base de données SQL Server** : Configuration initiale
- **Templates de base** : Interface utilisateur basique

### 🔧 Modifié
- **Configuration Django** : Settings de base
- **Modèles** : Structure initiale des entités comptables

### 📚 Documentation
- **README initial** : Description du projet
- **Requirements.txt** : Dépendances Python

---

## Types de modifications

- **✨ Ajouté** : Nouvelles fonctionnalités
- **🔧 Modifié** : Changements dans les fonctionnalités existantes
- **🐛 Corrigé** : Corrections de bugs
- **🔒 Sécurité** : Améliorations de sécurité
- **📚 Documentation** : Changements dans la documentation
- **🚀 Performance** : Améliorations de performance
- **🧪 Tests** : Ajout ou modification de tests
- **📦 Dépendances** : Mise à jour des dépendances
