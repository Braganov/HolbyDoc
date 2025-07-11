# Guide d'Installation et d'Utilisation de HolbyDoc

## Prérequis
- Python 3.11
- pip (gestionnaire de paquets Python)
- Git (pour cloner le repository)

## Installation

1. Cloner le repository :
```bash
git clone <url_du_repo>
cd HolbyDoc
```

2. Créer un environnement virtuel Python :
```bash
python3.11 -m venv venv
```

3. Activer l'environnement virtuel :
- Sur Linux/Mac :
```bash
source venv/bin/activate
```
- Sur Windows :
```bash
.\venv\Scripts\activate
```

4. Installer les dépendances :
```bash
pip install -r requirements.txt
```

5. Créer la base de données :
```bash
python create_db.py
```

## Configuration

1. Variables d'environnement (optionnel) :
- Créer un fichier `.env` à la racine du projet
- Ajouter les variables nécessaires :
```
SECRET_KEY=votre_clé_secrète
SQLALCHEMY_DATABASE_URI=sqlite:///holbydoc.db
```

## Lancement de l'Application

1. Démarrer le serveur de développement :
```bash
python run.py
```

2. Accéder à l'application :
- Ouvrir un navigateur web
- Aller à l'adresse : http://localhost:5000

## Utilisation

### Création d'un Compte
1. Cliquer sur "Register" dans la barre de navigation
2. Remplir le formulaire avec :
   - Prénom
   - Nom
   - Nom d'utilisateur
   - Email
   - Mot de passe (8 caractères minimum, avec majuscules, minuscules, chiffres et caractères spéciaux)

### Création d'un Cours
1. Se connecter à votre compte
2. Aller dans le "Dashboard"
3. Cliquer sur "New Course"
4. Remplir les informations du cours :
   - Titre
   - Description
   - Icône (format jpg ou png)

### Création d'une Leçon
1. Se connecter à votre compte
2. Aller dans le "Dashboard"
3. Sélectionner "New Lesson"
4. Remplir les informations :
   - Sélectionner le cours
   - Titre de la leçon
   - Slug (URL-friendly)
   - Contenu (utilisant l'éditeur CKEditor)
   - Image de couverture

## Fonctionnalités

- Système d'authentification complet
- Gestion des cours et des leçons
- Éditeur de texte riche (CKEditor)
- Système de fichiers pour les images
- Interface responsive

## Résolution des Problèmes Courants

1. Erreur de base de données :
   - Vérifier que `create_db.py` a été exécuté
   - Vérifier les permissions du dossier

2. Problèmes d'installation des dépendances :
   - Vérifier la version de Python (3.11 recommandée)
   - Mettre à jour pip : `pip install --upgrade pip`

3. Problèmes d'upload d'images :
   - Vérifier les permissions du dossier static/user_pics
   - Vérifier que le format est bien jpg ou png

## Support

Pour toute question ou problème, vous pouvez :
1. Ouvrir une issue sur GitHub
2. Contacter l'équipe de développement
3. Consulter la documentation technique dans le dossier Holberton_report/

## Sécurité

- Ne jamais partager votre SECRET_KEY
- Utiliser des mots de passe forts
- Mettre à jour régulièrement les dépendances
- Faire attention aux permissions des fichiers