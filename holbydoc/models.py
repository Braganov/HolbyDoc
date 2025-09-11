# Importation des modules nécessaires
from datetime import datetime  # Pour les horodatages
from holbydoc import db, login_manager  # Import des instances Flask
from flask_login import UserMixin  # Classe de base pour la gestion des utilisateurs
from itsdangerous import URLSafeTimedSerializer as Serializer  # Pour les tokens sécurisés
from flask import current_app

# Décorateur pour charger un utilisateur depuis la base de données
@login_manager.user_loader
def load_user(user_id):
    """Charge un utilisateur depuis la base de données par son ID"""
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """Modèle de données pour les utilisateurs
    
    Hérite de db.Model (SQLAlchemy) et UserMixin (Flask-Login)
    pour la gestion des sessions utilisateur
    """
    
    # Champs de la table users
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique
    fname = db.Column(db.String(25), nullable=False)  # Prénom
    lname = db.Column(db.String(25), nullable=False)  # Nom
    username = db.Column(db.String(25), unique=True, nullable=False)  # Nom d'utilisateur
    email = db.Column(db.String(125), unique=True, nullable=False)  # Email
    image_file = db.Column(db.String(20), nullable=False, default="default.png")  # Photo de profil
    bio = db.Column(db.Text, nullable=True)  # Biographie (optionnelle)
    password = db.Column(db.String(60), nullable=False)  # Mot de passe hashé
    lessons = db.relationship("Lesson", backref="author", lazy=True)  # Relation avec les leçons

    def get_reset_token(self):
        """Génère un token sécurisé pour la réinitialisation du mot de passe"""
        s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, age=3600):
        """Vérifie la validité d'un token de réinitialisation
        
        Args:
            token (str): Le token à vérifier
            age (int): Durée de validité en secondes (1h par défaut)
            
        Returns:
            User|None: L'utilisateur associé au token ou None si invalide
        """
        s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
        try:
            user_id = s.loads(token, max_age=age)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """Représentation string de l'objet User"""
        return f"User('{self.fname}', '{self.lname}', '{self.username}', '{self.email}', '{self.image_file}')"


class Lesson(db.Model):
    """Modèle de données pour les leçons"""
    
    # Champs de la table lessons
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique
    title = db.Column(db.String(100), nullable=False)  # Titre de la leçon
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Date de création
    content = db.Column(db.Text, nullable=False)  # Contenu de la leçon
    thumbnail = db.Column(
        db.String(20), nullable=False, default="default_thumbnail.jpg"  # Image de couverture
    )
    slug = db.Column(db.String(32), nullable=False)  # URL-friendly version du titre
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # Auteur (clé étrangère)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)  # Cours parent (clé étrangère)

    def __repr__(self):
        """Représentation string de l'objet Lesson"""
        return f"Lesson('{self.title}', '{self.date_posted}')"


class Course(db.Model):
    """Modèle de données pour les cours
    
    Un cours contient plusieurs leçons et organise le contenu de manière structurée
    """
    
    # Champs de la table courses
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique
    title = db.Column(db.String(50), unique=True, nullable=False)  # Titre du cours
    description = db.Column(db.String(150), nullable=False)  # Description courte
    icon = db.Column(db.String(20), nullable=False, default="default_icon.jpg")  # Icône du cours
    lessons = db.relationship("Lesson", backref="course_name", lazy=True)  # Relation avec les leçons

    def __repr__(self):
        """Représentation string de l'objet Course"""
        return f"Course('{self.title}')"