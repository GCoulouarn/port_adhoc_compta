# 📚 Documentation - Port Adhoc Compta

## 🎯 Vue d'ensemble

**Port Adhoc Compta** est une application Django de gestion comptable avec un système de libellés dynamiques et d'ordre d'affichage personnalisable. L'application permet de gérer les sociétés, devises, plans comptables et autres entités comptables avec une interface d'administration entièrement personnalisable.

## 🚀 Fonctionnalités principales

### 1. **Système de libellés dynamiques**
- ✅ **Gestion centralisée** : Tous les libellés sont stockés dans la table `AdminText`
- ✅ **Multilingue** : Support du français et de l'anglais
- ✅ **Templates personnalisés** : Interface d'administration entièrement personnalisable
- ✅ **Sections dynamiques** : Noms des sections modifiables ("Comptabilité" → "Finance Consolidation")

### 2. **Ordre d'affichage des modèles**
- ✅ **Contrôle total** : Ordre d'affichage des modèles par section
- ✅ **Interface éditable** : Modification directe dans l'admin
- ✅ **Tri automatique** : JavaScript pour réorganiser les modèles
- ✅ **Persistance** : Sauvegarde en base de données

### 3. **Gestion des devises et sociétés**
- ✅ **Relation ForeignKey** : Lien entre Societe et Devise
- ✅ **Affichage enrichi** : Devise visible dans la liste des sociétés
- ✅ **Filtres et recherche** : Par devise dans l'admin des sociétés
- ✅ **Formulaires organisés** : Champs groupés par catégorie

## 🏗️ Architecture technique

### **Applications Django**

#### `comptabilite/`
Application principale de gestion comptable.

**Modèles :**
- `Societe` : Gestion des sociétés avec relation vers Devise
- `Devise` : Gestion des devises (EUR, USD, etc.)
- `NatureCompte` : Natures de comptes
- `PlanCompteGroupe` : Groupes de plans comptables
- `PlanCompteLocal` : Plans comptables locaux
- `Stade` : Stades de traitement
- `TypeValeur` : Types de valeurs

**Admin personnalisé :**
- `SocieteAdmin` : Affichage de la devise, filtres, recherche
- `DeviseAdmin` : Gestion des devises avec libellés dynamiques

#### `parametres/`
Application de gestion des paramètres et libellés.

**Modèles :**
- `AdminText` : Libellés dynamiques avec ordre d'affichage

**Admin personnalisé :**
- `AdminTextAdmin` : Gestion des libellés avec ordre d'affichage éditable

### **Middleware et Processors**

#### `AdminLabelMiddleware`
- **Fonction** : Applique les libellés dynamiques aux modèles
- **Timing** : S'exécute sur chaque requête admin
- **Performance** : Cache des libellés pour optimiser les performances

#### `admin_labels` (Context Processor)
- **Fonction** : Injecte les libellés dans tous les templates
- **Structure** : Crée une hiérarchie `admin_labels.section.comptabilite`
- **Fallback** : Gestion des langues avec fallback français

### **Templates personnalisés**

#### `templates/admin/base_site.html`
- **Titre dynamique** : Utilise `admin_labels.site.title`
- **Header personnalisé** : Utilise `admin_labels.site.header`
- **CSS** : Masque le sélecteur de langue natif

#### `templates/admin/app_list.html`
- **Sections dynamiques** : Noms des sections personnalisables
- **Modèles dynamiques** : Libellés des modèles personnalisables
- **Tri JavaScript** : Réorganise les modèles selon l'ordre défini

## 🗄️ Base de données

### **Table `T_E_AdminText_ADT`**
```sql
CREATE TABLE T_E_AdminText_ADT (
    ADT_Id INT PRIMARY KEY IDENTITY(1,1),
    ADT_Language VARCHAR(5) DEFAULT 'fr',
    ADT_Key VARCHAR(100),
    ADT_Value VARCHAR(255),
    ADT_DisplayOrder INT DEFAULT 0
);
```

**Clés principales :**
- `site.title` : Titre du site
- `site.header` : En-tête de l'admin
- `section.comptabilite` : Nom de la section comptabilité
- `section.parametres` : Nom de la section paramètres
- `model.Devise.name_plural` : Libellé pluriel des devises
- `model.Societe.name_plural` : Libellé pluriel des sociétés

### **Relation Devise-Société**
```sql
-- Colonne ajoutée à T_E_Societe_SOC
ALTER TABLE T_E_Societe_SOC 
ADD DEV_Id INT REFERENCES T_E_Devises_DEV(DEV_Id);
```

## ⚙️ Configuration

### **Settings.py**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'comptabilite',
    'parametres',  # Nouvelle application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'comptabilite.middleware.AdminLabelMiddleware',  # Middleware personnalisé
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'comptabilite.context_processors.admin_labels',  # Context processor
            ],
        },
    },
]
```

## 🎨 Interface utilisateur

### **Page d'accueil admin**
- **Titre** : "Port Adhoc" (configurable)
- **Sections** : 
  - "Finance Consolidation" (au lieu de "Comptabilité")
  - "Paramètres" (nouvelle section)
- **Modèles triés** : Selon l'ordre défini dans `AdminText`

### **Gestion des libellés**
1. **Accès** : Admin → Paramètres → Libellés Admin
2. **Modification** : Édition directe des libellés et ordres
3. **Application** : Changements immédiats dans l'interface

### **Gestion des sociétés**
1. **Liste enrichie** : Affichage de la devise
2. **Filtres** : Par devise, groupe, statut
3. **Recherche** : Par code, intitulé, devise
4. **Formulaire** : Champs organisés par catégorie

## 🚀 Installation et déploiement

### **Prérequis**
- Python 3.12+
- Django 5.0.6
- SQL Server (avec pyodbc)
- Virtual environment

### **Installation**
```bash
# Cloner le repository
git clone https://github.com/GCoulouarn/port_adhoc_compta.git
cd port_adhoc_compta

# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configuration de la base de données
# Modifier .env avec vos paramètres SQL Server

# Migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Démarrer le serveur
python manage.py runserver
```

### **Configuration de la base de données**
```env
# .env
DB_ENGINE=mssql
DB_HOST=your-server
DB_PORT=1433
DB_NAME=your-database
DB_USER=your-username
DB_PASSWORD=your-password
```

## 📝 Utilisation

### **Personnalisation des libellés**

1. **Accéder à l'admin** : `http://localhost:8000/admin/`
2. **Section Paramètres** → **Libellés Admin**
3. **Modifier les libellés** :
   - `site.title` : Titre du site
   - `section.comptabilite` : Nom de la section comptabilité
   - `model.Devise.name_plural` : Libellé des devises
4. **Ajuster l'ordre** : Modifier la colonne "Ordre d'affichage"

### **Gestion des sociétés**

1. **Section Finance Consolidation** → **Sociétés**
2. **Ajouter une société** : Remplir les informations + sélectionner la devise
3. **Filtrer par devise** : Utiliser le filtre "Devise"
4. **Rechercher** : Par code, intitulé ou nom de devise

## 🔧 Développement

### **Ajout de nouveaux libellés**

1. **Ajouter en base** :
```python
AdminText.objects.create(
    language='fr',
    key='model.NouveauModele.name_plural',
    value='Nouveaux Modèles',
    display_order=10
)
```

2. **Utiliser dans les templates** :
```html
{{ admin_labels.model.NouveauModele.name_plural|default:"Modèles" }}
```

### **Ajout de nouveaux modèles**

1. **Créer le modèle** avec `DynamicLabelsMixin`
2. **Ajouter l'admin** avec `AdminLabelMixin`
3. **Créer les libellés** dans `AdminText`
4. **Mettre à jour** `templates/admin/app_list.html`

## 🐛 Dépannage

### **Problèmes courants**

1. **Libellés non appliqués** :
   - Vérifier que `AdminLabelMiddleware` est dans `MIDDLEWARE`
   - Vérifier que `admin_labels` est dans les context processors

2. **Ordre d'affichage incorrect** :
   - Vérifier les valeurs `display_order` dans `AdminText`
   - Vérifier que le JavaScript est chargé

3. **Erreurs de base de données** :
   - Vérifier la connexion SQL Server
   - Exécuter `python manage.py migrate`

### **Logs et débogage**

```bash
# Mode debug
python manage.py runserver --verbosity=2

# Vérifier la configuration
python manage.py check

# Vérifier les migrations
python manage.py showmigrations
```

## 📊 Performance

### **Optimisations implémentées**

1. **Cache des libellés** : Évite les requêtes répétées
2. **Middleware optimisé** : Exécution uniquement sur les requêtes admin
3. **Requêtes groupées** : Récupération de tous les libellés en une fois

### **Métriques recommandées**

- **Temps de réponse** : < 200ms pour les pages admin
- **Requêtes DB** : < 10 par page admin
- **Taille des templates** : Optimisation des context processors

## 🔒 Sécurité

### **Mesures implémentées**

1. **Authentification** : Système Django standard
2. **Autorisation** : Permissions par modèle
3. **CSRF Protection** : Tokens CSRF activés
4. **Validation** : Validation des données d'entrée

### **Recommandations**

1. **HTTPS** : Utiliser en production
2. **Secrets** : Variables d'environnement pour les mots de passe
3. **Backup** : Sauvegarde régulière de la base de données

## 📈 Évolutions futures

### **Fonctionnalités prévues**

1. **Multilingue complet** : Support de toutes les langues
2. **Thèmes** : Système de thèmes personnalisables
3. **API REST** : Interface API pour intégrations
4. **Rapports** : Génération de rapports PDF/Excel
5. **Audit** : Traçabilité des modifications

### **Améliorations techniques**

1. **Tests unitaires** : Couverture de test complète
2. **CI/CD** : Pipeline de déploiement automatique
3. **Monitoring** : Surveillance des performances
4. **Documentation API** : Documentation Swagger/OpenAPI

## 📞 Support

### **Contact**
- **Développeur** : Gilles Coulouarn
- **Repository** : https://github.com/GCoulouarn/port_adhoc_compta
- **Issues** : Utiliser le système d'issues GitHub

### **Contribution**
1. Fork le repository
2. Créer une branche feature
3. Implémenter les modifications
4. Créer une Pull Request

---

**Version** : 1.0.0  
**Dernière mise à jour** : 15 septembre 2025  
**Django** : 5.0.6  
**Python** : 3.12+
