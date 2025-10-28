# 📚 HolbyDoc

> **Plateforme éducative centralisée pour Holberton School**  
> Une solution complète de gestion et partage de ressources pédagogiques

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 Table des matières

- [À propos](#-à-propos)
- [Contexte du projet](#-contexte-du-projet)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture technique](#-architecture-technique)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Sécurité](#-sécurité)
- [Déploiement](#-déploiement)
- [Roadmap](#-roadmap)
- [Contribution](#-contribution)
- [Auteur](#-auteur)
- [Licence](#-licence)

---

## 🎯 À propos

**HolbyDoc** est une plateforme web full-stack développée pour centraliser et organiser les ressources d'apprentissage destinées aux étudiants de Holberton School. Face à la fragmentation des informations pédagogiques, HolbyDoc offre un environnement structuré où les utilisateurs peuvent consulter des cours organisés, créer du contenu enrichi et partager leurs connaissances.

### Problème résolu

Les étudiants de Holberton School font face à :
- Une documentation dispersée entre plateforme officielle, ressources externes et échanges informels
- Des concepts techniques avancés nécessitant des explications adaptées
- Un besoin de centralisation pour optimiser l'apprentissage dans un programme intensif

HolbyDoc répond à ces défis en proposant une plateforme unifiée, intuitive et collaborative.

---

## 🌍 Contexte du projet

Ce projet a été réalisé dans le cadre du titre professionnel **RNCP5 "Développeur Web et Web Mobile"** et démontre une maîtrise complète du développement full-stack :

- ✅ **Frontend** : Interface responsive avec HTML5, CSS3, Bootstrap 5
- ✅ **Backend** : Architecture MVC avec Flask et blueprints
- ✅ **Base de données** : Modélisation relationnelle avec SQLAlchemy
- ✅ **Sécurité** : Authentification Flask-Login, protection CSRF, hachage Bcrypt
- ✅ **Déploiement** : Infrastructure Linux avec Nginx et Gunicorn

---

## ✨ Fonctionnalités

### 👤 Gestion des utilisateurs
- Inscription et authentification sécurisée
- Gestion de profil avec upload de photo
- Système de rôles (utilisateur, contributeur, administrateur)
- Récupération de mot de passe

### 📖 Gestion du contenu pédagogique
- Création et organisation de cours par thématiques
- Leçons détaillées avec contenu enrichi
- Éditeur WYSIWYG intégré (CKEditor)
- Upload et gestion d'images et médias
- Navigation hiérarchique intuitive

### 🔒 Sécurité avancée
- Hachage des mots de passe avec Bcrypt
- Protection CSRF sur tous les formulaires
- Validation des données côté serveur
- Sanitization du contenu HTML
- Sessions sécurisées avec Flask-Login

### 🎨 Interface utilisateur
- Design responsive adapté à tous les appareils
- Navigation intuitive avec fil d'Ariane
- Dashboard personnalisé pour chaque utilisateur
- Messages flash pour le feedback utilisateur

---

## 🏗️ Architecture technique

### Stack technologique

**Backend**
- Python 3.11
- Flask 2.0.3 (framework web)
- SQLAlchemy (ORM)
- Flask-Login (authentification)
- Flask-WTF (formulaires et CSRF)
- Flask-Bcrypt (hachage des mots de passe)
- Flask-CKEditor (éditeur de contenu)

**Frontend**
- HTML5 & CSS3
- Bootstrap 5.1.3
- Bootstrap Icons 1.8.1
- JavaScript
- Jinja2 (templates)

**Base de données**
- SQLite (développement)
- PostgreSQL (production)

**Infrastructure**
- Nginx (proxy inverse)
- Gunicorn (serveur WSGI)
- Let's Encrypt (certificats SSL)

### Architecture MVC

```
┌─────────────────┐
│   Utilisateur   │
└────────┬────────┘
         │
    ┌────▼────┐
    │  Nginx  │  ← Proxy inverse & fichiers statiques
    └────┬────┘
         │
   ┌─────▼──────┐
   │  Gunicorn  │  ← Serveur WSGI
   └─────┬──────┘
         │
   ┌─────▼──────┐
   │   Flask    │  ← Application (MVC)
   └─────┬──────┘
         │
   ┌─────▼──────┐
   │ PostgreSQL │  ← Base de données
   └────────────┘
```

---

## 🚀 Installation

### Prérequis

- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)
- Git
- Environnement virtuel Python

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/Braganov/HolbyDoc.git
cd HolbyDoc
```

2. **Créer et activer l'environnement virtuel**
```bash
python3.11 -m venv venv

# Sur Linux/Mac
source venv/bin/activate

# Sur Windows
.\venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
# Créer un fichier .env à la racine
echo "SECRET_KEY=votre_clé_secrète_très_longue" > .env
echo "SQLALCHEMY_DATABASE_URI=sqlite:///holbydoc.db" >> .env
```

5. **Initialiser la base de données**
```bash
python create_db.py
```

6. **Lancer l'application**
```bash
python run.py
```

7. **Accéder à l'application**
Ouvrez votre navigateur : `http://localhost:5000`

---

## 📖 Utilisation

### Inscription
1. Cliquer sur "Register" dans la barre de navigation
2. Remplir le formulaire avec vos informations
3. Valider pour créer votre compte

### Connexion
1. Cliquer sur "Login"
2. Saisir email et mot de passe
3. Accéder au dashboard personnalisé

### Créer un cours
1. Se connecter à votre compte
2. Aller dans "Dashboard"
3. Cliquer sur "New Course"
4. Remplir les informations (titre, description, icône)

### Créer une leçon
1. Sélectionner un cours
2. Cliquer sur "New Lesson"
3. Utiliser l'éditeur CKEditor pour créer du contenu enrichi
4. Ajouter une image de couverture
5. Publier

---

## 📂 Structure du projet

```
HolbyDoc/
│
├── holbydoc/                    # Package principal
│   ├── __init__.py             # Application factory
│   ├── config.py               # Configuration
│   ├── models.py               # Modèles SQLAlchemy
│   ├── forms.py                # Formulaires WTForms
│   ├── helpers.py              # Fonctions utilitaires
│   │
│   ├── main/                   # Blueprint principal
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── users/                  # Blueprint utilisateurs
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── helpers.py
│   │
│   ├── courses/                # Blueprint cours
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── lessons/                # Blueprint leçons
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── helpers.py
│   │
│   ├── errors/                 # Gestion des erreurs
│   │   ├── __init__.py
│   │   └── handlers.py
│   │
│   ├── static/                 # Fichiers statiques
│   │   ├── main.css
│   │   ├── ckeditor/
│   │   ├── course_icons/
│   │   ├── lesson_thumbnails/
│   │   └── user_pics/
│   │
│   └── templates/              # Templates Jinja2
│       ├── layout.html
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── dashboard.html
│       ├── course.html
│       ├── lesson.html
│       └── errors/
│
├── Holberton_report/           # Documentation technique
├── venv/                       # Environnement virtuel
├── create_db.py                # Script d'initialisation DB
├── run.py                      # Point d'entrée
├── requirements.txt            # Dépendances Python
├── GUIDE.md                    # Guide d'utilisation détaillé
└── README.md                   # Ce fichier
```

---

## 🔒 Sécurité

HolbyDoc implémente plusieurs mesures de sécurité essentielles :

### Authentification
- Hachage des mots de passe avec **Bcrypt** et sel unique
- Sessions sécurisées avec **Flask-Login**
- Cookies avec flags `HttpOnly` et `Secure`
- Système de récupération de mot de passe sécurisé

### Protection des données
- **Protection CSRF** sur tous les formulaires
- **Validation des données** côté serveur avec WTForms
- **Échappement automatique** des contenus avec Jinja2
- **Sanitization HTML** pour le contenu CKEditor

### Prévention des attaques
- Protection contre les **injections SQL** via ORM SQLAlchemy
- Protection contre les **attaques XSS** (Cross-Site Scripting)
- **Upload sécurisé** avec validation du type MIME
- Variables d'environnement pour les **secrets**

### Contrôle d'accès
- Système de **rôles** (user, contributor, admin)
- Décorateurs `@login_required` pour routes protégées
- Vérification des **permissions** avant modification

---

## 🌐 Déploiement

### Configuration de production

1. **Serveur Linux** (Ubuntu recommandé)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv nginx postgresql
```

2. **Configuration PostgreSQL**
```bash
sudo -u postgres createdb holbydoc
sudo -u postgres createuser holbydoc_user
```

3. **Installation Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:8000 run:app
```

4. **Configuration Nginx**
```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /chemin/vers/holbydoc/holbydoc/static;
    }
}
```

5. **Certificat SSL avec Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com
```

Pour plus de détails, consultez le [GUIDE.md](GUIDE.md).

---

## 🗺️ Roadmap

### Court terme
- [ ] Système de recherche avancée avec filtres
- [ ] Espace de discussion (commentaires sous les leçons)
- [ ] Système de favoris et parcours personnalisés

### Moyen terme
- [ ] API REST pour intégrations tierces
- [ ] Application mobile (PWA)
- [ ] Notifications en temps réel

### Long terme
- [ ] Système de quiz et évaluations
- [ ] IA pour recommandations de contenu
- [ ] Support multilingue
- [ ] Forum communautaire intégré

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Standards de code
- Suivre les conventions **PEP 8** pour Python
- Documenter les fonctions avec des docstrings
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation si nécessaire

---

## 👨‍💻 Auteur

**Ibrahim Houmaidi**
- Formation : Holberton School Paris - Promo C17 (2023-2024)
- Certification : RNCP5 "Développeur Web et Web Mobile"
- GitHub : [@Braganov](https://github.com/Braganov)
- Email : ibrahim.houmaidi@example.com

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **Holberton School** pour la formation et l'accompagnement
- La communauté **Flask** pour la documentation et les ressources
- Tous les **étudiants** qui ont testé et fourni des retours
- Les **contributeurs** open source des bibliothèques utilisées

---

## 📚 Documentation additionnelle

- [Guide d'installation détaillé](GUIDE.md)
- [Documentation technique](Holberton_report/)
- [Captures d'écran](Holberton_report/screenshots/)
- [Diagrammes UML](Holberton_report/diagrams/)

---

## 🌟 Support

Si vous trouvez ce projet utile, n'hésitez pas à :
- ⭐ Mettre une étoile sur GitHub
- 🐛 Signaler des bugs via les Issues
- 💡 Proposer des améliorations
- 📢 Partager avec d'autres étudiants

---

**Fait avec ❤️ pour la communauté Holberton School**

*[View English version](./README_EN.md) | [Voir la version française](./README_FR.md)*
