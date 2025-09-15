# 🏦 Port Adhoc Compta

> Application Django de gestion comptable avec libellés dynamiques et interface personnalisable

[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-2019+-red.svg)](https://microsoft.com/sql-server)

## ✨ Fonctionnalités principales

### 🎨 **Interface personnalisable**
- **Libellés dynamiques** : Tous les textes de l'interface sont modifiables
- **Ordre d'affichage** : Contrôle total de l'ordre des modèles par section
- **Sections personnalisées** : "Comptabilité" → "Finance Consolidation"
- **Templates sur mesure** : Interface d'administration entièrement personnalisée

### 🏢 **Gestion comptable**
- **Sociétés** : Gestion complète avec relation aux devises
- **Devises** : Support multi-devises (EUR, USD, etc.)
- **Plans comptables** : Groupes et plans locaux
- **Natures de comptes** : Classification des comptes

### 🔧 **Administration avancée**
- **Filtres intelligents** : Par devise, groupe, statut
- **Recherche globale** : Par code, intitulé, devise
- **Formulaires organisés** : Champs groupés par catégorie
- **Interface responsive** : Optimisée pour tous les écrans

## 🚀 Démarrage rapide

### Prérequis
- Python 3.12+
- SQL Server 2019+
- Git

### Installation

```bash
# 1. Cloner le repository
git clone https://github.com/GCoulouarn/port_adhoc_compta.git
cd port_adhoc_compta

# 2. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configuration de la base de données
cp .env.example .env
# Modifier .env avec vos paramètres SQL Server

# 5. Migrations
python manage.py migrate

# 6. Créer un superutilisateur
python manage.py createsuperuser

# 7. Démarrer le serveur
python manage.py runserver
```

### Accès
- **Application** : http://localhost:8000/
- **Administration** : http://localhost:8000/admin/

## 📋 Configuration

### Variables d'environnement (.env)
```env
# Base de données SQL Server
DB_ENGINE=mssql
DB_HOST=your-server
DB_PORT=1433
DB_NAME=your-database
DB_USER=your-username
DB_PASSWORD=your-password

# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Configuration des libellés
1. Accéder à **Admin** → **Paramètres** → **Libellés Admin**
2. Modifier les libellés selon vos besoins :
   - `site.title` : Titre du site
   - `section.comptabilite` : Nom de la section comptabilité
   - `model.Devise.name_plural` : Libellé des devises
3. Ajuster l'ordre d'affichage des modèles

## 🏗️ Architecture

### Applications
- **`comptabilite/`** : Gestion comptable principale
- **`parametres/`** : Gestion des libellés et paramètres

### Composants clés
- **`AdminLabelMiddleware`** : Application des libellés dynamiques
- **`admin_labels`** : Context processor pour les templates
- **Templates personnalisés** : Interface d'administration sur mesure

## 📊 Modèles de données

### Sociétés
```python
class Societe(models.Model):
    code = models.CharField(max_length=20)
    intitule = models.CharField(max_length=100)
    devise = models.ForeignKey('Devise', ...)  # Relation vers devise
    groupe = models.CharField(max_length=50)
    archive = models.BooleanField(default=False)
```

### Devises
```python
class Devise(models.Model):
    code_iso = models.CharField(max_length=3)
    intitule = models.CharField(max_length=20)
    sigle = models.CharField(max_length=3)
```

### Libellés dynamiques
```python
class AdminText(models.Model):
    language = models.CharField(max_length=5, default='fr')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    display_order = models.IntegerField(default=0)
```

## 🎨 Personnalisation

### Modifier les libellés
1. **Interface admin** : Admin → Paramètres → Libellés Admin
2. **Clés disponibles** :
   - `site.title` : Titre du site
   - `site.header` : En-tête de l'admin
   - `section.comptabilite` : Nom de la section comptabilité
   - `model.*.name_plural` : Libellés des modèles

### Ajouter de nouveaux modèles
1. Créer le modèle avec `DynamicLabelsMixin`
2. Ajouter l'admin avec `AdminLabelMixin`
3. Créer les libellés dans `AdminText`
4. Mettre à jour `templates/admin/app_list.html`

## 🔧 Développement

### Structure du projet
```
port_adhoc_compta/
├── comptabilite/          # App principale
│   ├── models.py         # Modèles comptables
│   ├── admin.py          # Configuration admin
│   ├── middleware.py     # Middleware libellés
│   └── context_processors.py
├── parametres/           # App paramètres
│   ├── models.py         # Modèle AdminText
│   └── admin.py          # Admin des libellés
├── templates/admin/      # Templates personnalisés
├── requirements.txt      # Dépendances Python
└── DOCUMENTATION.md      # Documentation complète
```

### Commandes utiles
```bash
# Vérifier la configuration
python manage.py check

# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic

# Créer un superutilisateur
python manage.py createsuperuser
```

## 🐛 Dépannage

### Problèmes courants

**Libellés non appliqués**
- Vérifier que `AdminLabelMiddleware` est dans `MIDDLEWARE`
- Vérifier que `admin_labels` est dans les context processors

**Erreurs de base de données**
- Vérifier la connexion SQL Server
- Exécuter `python manage.py migrate`

**Ordre d'affichage incorrect**
- Vérifier les valeurs `display_order` dans `AdminText`
- Vérifier que le JavaScript est chargé

### Logs et débogage
```bash
# Mode debug
python manage.py runserver --verbosity=2

# Vérifier les migrations
python manage.py showmigrations

# Shell Django
python manage.py shell
```

## 📈 Performance

### Optimisations
- **Cache des libellés** : Évite les requêtes répétées
- **Middleware optimisé** : Exécution uniquement sur les requêtes admin
- **Requêtes groupées** : Récupération de tous les libellés en une fois

### Métriques recommandées
- **Temps de réponse** : < 200ms pour les pages admin
- **Requêtes DB** : < 10 par page admin

## 🔒 Sécurité

### Mesures implémentées
- Authentification Django standard
- Protection CSRF
- Validation des données d'entrée
- Permissions par modèle

### Recommandations production
- Utiliser HTTPS
- Variables d'environnement pour les secrets
- Sauvegarde régulière de la base de données

## 📚 Documentation

- **[Documentation complète](DOCUMENTATION.md)** : Guide détaillé du projet
- **[API Django](https://docs.djangoproject.com/)** : Documentation officielle Django
- **[SQL Server](https://docs.microsoft.com/sql/)** : Documentation Microsoft SQL Server

## 🤝 Contribution

1. Fork le repository
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commiter les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Pousser vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Gilles Coulouarn**
- GitHub: [@GCoulouarn](https://github.com/GCoulouarn)
- Email: [votre-email@example.com]

## 🙏 Remerciements

- [Django](https://djangoproject.com/) - Framework web Python
- [Microsoft SQL Server](https://microsoft.com/sql-server) - Base de données
- [Bootstrap](https://getbootstrap.com/) - Framework CSS

---

**Version** : 1.0.0  
**Dernière mise à jour** : 15 septembre 2025  
**Django** : 5.0.6  
**Python** : 3.12+