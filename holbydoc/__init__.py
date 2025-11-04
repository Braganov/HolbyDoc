# Importation des modules nécessaires
import os
from flask import Flask  # Framework web Python
from flask_sqlalchemy import SQLAlchemy  # ORM pour la base de données
from flask_bcrypt import Bcrypt  # Pour le hachage des mots de passe
from flask_login import LoginManager  # Gestion de l'authentification
from flask_migrate import Migrate  # Pour les migrations de base de données
from flask_ckeditor import CKEditor  # Éditeur de texte riche
from flask_modals import Modal  # Pour les fenêtres modales
from flask_mail import Mail  # Pour l'envoi d'emails
from holbydoc.config import Config  # Configuration de l'application
from flask_admin import Admin  # Interface d'administration


# Initialisation des extensions Flask
db = SQLAlchemy()  # Instance de la base de données
bcrypt = Bcrypt()  # Instance pour le hachage
migrate = Migrate(db)  # Instance pour les migrations
login_manager = LoginManager()  # Instance pour la gestion de connexion
ckeditor = CKEditor()  # Instance de l'éditeur
modal = Modal()  # Instance pour les modales
login_manager.login_view = "users.login"  # Page de connexion par défaut
login_manager.login_message_category = "info"  # Catégorie des messages de connexion
mail = Mail()  # Instance pour les emails
admin = Admin()  # Instance pour l'administration


def create_app(config_calss=Config):
    """Fonction de création de l'application Flask"""
    app = Flask(__name__)  # Création de l'instance Flask
    app.config.from_object(Config)  # Chargement de la configuration
    from holbydoc.adminbp.routes import MyAdminIndexView  # Import de la vue admin

    # Initialisation des extensions avec l'application
    db.init_app(app)  # Base de données
    bcrypt.init_app(app)  # Hachage
    login_manager.init_app(app)  # Gestion de connexion
    ckeditor.init_app(app)  # Éditeur
    modal.init_app(app)  # Modales
    mail.init_app(app)  # Emails
    admin.init_app(app, index_view=MyAdminIndexView())  # Admin

    # Importation des routes
    from holbydoc.main.routes import main  # Routes principales
    from holbydoc.users.routes import users  # Routes utilisateurs
    from holbydoc.lessons.routes import lessons  # Routes des leçons
    from holbydoc.courses.routes import courses_bp  # Routes des cours
    from holbydoc.errors.handlers import errors  # Gestion des erreurs
    from holbydoc.adminbp.routes import adminbp  # Routes admin

    # Enregistrement des blueprints
    app.register_blueprint(adminbp)  # Administration
    app.register_blueprint(main)  # Principal
    app.register_blueprint(users)  # Utilisateurs
    app.register_blueprint(lessons)  # Leçons
    app.register_blueprint(courses_bp)  # Cours
    app.register_blueprint(errors)  # Erreurs

    return app  # Retourne l'application configurée