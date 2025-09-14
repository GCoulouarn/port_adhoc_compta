# Port Adhoc Compta

Application web Django de gestion comptable, migrée depuis une application C# WinForms.

## 🚀 Fonctionnalités

- **Gestion des sociétés** : CRUD complet avec tri et filtrage
- **Gestion des devises** : CRUD complet avec tri et filtrage
- **Système d'authentification** : Connexion, inscription, gestion des profils
- **Gestion des permissions** : Groupes d'utilisateurs avec droits spécifiques
- **Interface responsive** : Bootstrap 5 pour une expérience utilisateur optimale
- **API REST** : Endpoints pour l'intégration avec d'autres systèmes
- **Base de données SQL Server** : Intégration avec mssql-django

## 🛠️ Technologies

- **Backend** : Django 5.2.6, Django REST Framework
- **Base de données** : SQL Server (mssql-django, pyodbc)
- **Frontend** : HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentification** : Django Auth avec groupes et permissions
- **API** : Django REST Framework

## 📋 Prérequis

- Python 3.8+
- SQL Server
- pip

## 🔧 Installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd port_adhoc_compta
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv port_adhoc_compta_env
   source port_adhoc_compta_env/bin/activate  # Linux/Mac
   # ou
   port_adhoc_compta_env\Scripts\activate  # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   - Modifier les paramètres de connexion dans `port_adhoc_compta/settings.py`
   - Host: `172.31.0.5,60322`
   - Database: `TEST_TDB`
   - User: `Dev_Cube_Web`
   - Password: `G4L|pK$9tbal`

5. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

6. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

7. **Configurer les permissions**
   ```bash
   python setup_permissions.py
   ```

8. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

## 🌐 Accès

- **Application** : http://localhost:8000
- **Administration** : http://localhost:8000/admin

## 👥 Utilisateurs par défaut

- **Superutilisateur** : `admin` / `admin123`
- **Gestionnaire** : `Gilles` / `gilles123` (groupe "Gestionnaires")

## 📊 Modèles de données

### Societe
- `id` : Identifiant unique (non auto-incrémenté)
- `code` : Code de la société
- `intitule` : Nom de la société
- `groupe` : Indique si c'est un groupe
- `archive` : Indique si archivé
- `devise_id` : Référence vers la devise

### Devise
- `id` : Identifiant unique (non auto-incrémenté)
- `code_iso` : Code ISO à 3 lettres
- `intitule` : Nom de la devise
- `sigle` : Symbole de la devise

## 🔐 Permissions

Le système utilise les permissions Django standard :
- `add_societe`, `change_societe`, `delete_societe`, `view_societe`
- `add_devise`, `change_devise`, `delete_devise`, `view_devise`

## 🎯 Fonctionnalités principales

### Gestion des sociétés
- Liste avec tri par colonnes (ID, code, intitulé, groupe, archivé)
- Filtrage par recherche, type (groupe/société), statut (archivé/actif)
- Création, modification, suppression avec permissions
- Sélection de devise via dropdown

### Gestion des devises
- Liste avec tri par colonnes (ID, code ISO, intitulé, sigle)
- Filtrage par recherche
- Création, modification, suppression avec permissions

### Système d'authentification
- Connexion/déconnexion
- Inscription d'utilisateurs
- Gestion des profils
- Groupes avec permissions spécifiques

## 🔧 Configuration

### Base de données
```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'TEST_TDB',
        'HOST': '172.31.0.5,60322',
        'USER': 'Dev_Cube_Web',
        'PASSWORD': 'G4L|pK$9tbal',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}
```

### Permissions
Les permissions sont configurées via le script `setup_permissions.py` qui :
- Crée les permissions manquantes pour les devises
- Assigne les permissions au groupe "Gestionnaires"

## 📝 Notes techniques

- **Clés primaires non auto-incrémentées** : Gestion manuelle des IDs via requêtes SQL
- **Templates personnalisés** : Interface d'administration Django personnalisée
- **Tri dynamique** : URLs avec paramètres `sort` et `order`
- **Filtrage** : Utilisation de `Q` objects pour les requêtes complexes
- **Responsive design** : Bootstrap 5 pour l'adaptabilité mobile

## 🚀 Déploiement

Pour un déploiement en production :
1. Configurer les variables d'environnement
2. Utiliser un serveur WSGI/ASGI (Gunicorn, uWSGI)
3. Configurer un serveur web (Nginx, Apache)
4. Utiliser une base de données de production
5. Configurer HTTPS et la sécurité

## 📞 Support

Pour toute question ou problème, consultez la documentation Django ou contactez l'équipe de développement.
