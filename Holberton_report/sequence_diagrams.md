# HolbyDoc - Architecture et Flux de Données

## 1. Architecture Globale
```mermaid
graph TB
    Client[Client Browser]
    Server[Flask Server]
    Auth[Authentication System]
    DB[(SQLite Database)]
    Static[Static Files]
    
    Client --> Server
    Server --> Auth
    Server --> DB
    Server --> Static

    subgraph Static Files
        Images[Course/Lesson Images]
        Profile[User Pictures]
        Assets[CSS/Bootstrap]
    end

    style Client fill:#f0f0f0,stroke:#333,stroke-width:2px
    style Server fill:#e0e0e0,stroke:#333,stroke-width:2px
    style Auth fill:#d0d0d0,stroke:#333,stroke-width:2px
    style DB fill:#c0c0c0,stroke:#333,stroke-width:2px
    style Static fill:#b0b0b0,stroke:#333,stroke-width:2px
```

## 2. Flux de Données Global
```mermaid
sequenceDiagram
    participant Client as Navigateur
    participant Server as Flask Server
    participant Auth as Authentication
    participant DB as Database
    participant Static as Static Files

    Note over Client,Static: Flux principal de l'application
    
    Client->>Server: 1. Requête HTTP
    
    alt Accès public (cours/leçons)
        Server->>DB: 2a. Requête données publiques
        DB-->>Server: 3a. Retourne contenu
        Server->>Static: 4a. Récupère images associées
        Static-->>Server: 5a. Retourne images
        Server-->>Client: 6a. Affiche contenu avec images
    else Action protégée (création/édition)
        Server->>Auth: 2b. Vérifie session utilisateur
        Auth->>DB: 3b. Vérifie permissions
        
        alt Utilisateur authentifié
            DB-->>Auth: 4b. Accès autorisé
            Server->>DB: 5b. Exécute l'action
            alt Upload d'images
                Server->>Static: 6b. Sauvegarde images
            end
            DB-->>Server: 7b. Confirme action
            Server-->>Client: 8b. Retourne résultat
        else Non authentifié
            Auth-->>Server: 4c. Accès refusé
            Server-->>Client: 5c. Redirige vers login
        end
    end
```

## 3. Technologies Utilisées

### Frontend
- **HTML5/CSS3**
  - Structure sémantique
  - Design responsive
  - Classes CSS personnalisées

- **Jinja2 Templates**
  - Moteur de template pour Flask
  - Fonctionnalités principales utilisées :
    ```html
    {# Héritage de templates #}
    {% extends "layout.html" %}
    {% block content %}{% endblock %}

    {# Variables et expressions #}
    {{ title }}
    {{ url_for('static', filename='image.jpg') }}

    {# Conditions #}
    {% if current_user.is_authenticated %}
        <a href="{{ url_for('profile') }}">Profile</a>
    {% endif %}

    {# Boucles #}
    {% for course in courses %}
        <div class="card">{{ course.title }}</div>
    {% endfor %}
    ```

- **Bootstrap 5**
  - Grille responsive
  - Composants UI
  - Classes utilitaires
  - JavaScript de base (navigation mobile)

### Backend Framework
- **Flask**: Framework web principal
  - Routing système
  - Gestion des requêtes
  - Intégration native avec Jinja2

### Base de données
- **SQLite**: Stockage des données
  - Simple à configurer
  - Pas de serveur séparé nécessaire
  - Idéal pour MVP
- **SQLAlchemy**: ORM
  - Mapping objet-relationnel
  - Gestion des relations
  - Requêtes optimisées

### Authentification
- **Flask-Login**: Gestion des sessions
  - Décorateurs d'authentification (@login_required)
  - Gestion des sessions utilisateur
  - Protection des routes d'administration

### Gestion des formulaires
- **WTForms**: Validation des données
  - Validation côté serveur
  - Protection CSRF
  - Messages d'erreur personnalisés

### Édition de contenu
- **CKEditor**: Éditeur WYSIWYG
  - Support markdown
  - Upload d'images
  - Plugins personnalisables

### Gestion des Fichiers Statiques
- **Dossiers statiques**:
  - course_icons/ : Images des cours
  - lesson_thumbnails/ : Miniatures des leçons
  - user_pics/ : Photos de profil
  - media/ : Images des contenus (CKEditor)