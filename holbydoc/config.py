# Importation du module os pour accéder aux variables d'environnement
import os

class Config:
    """Classe de configuration de l'application Flask"""
   
    # Clé secrète pour la sécurité de l'application
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # URI de connexion à la base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # Activation du suivi des modifications SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Activation des snippets de code dans l'éditeur CKEditor
    CKEDITOR_ENABLE_CODESNIPPET = True
    # Configuration du gestionnaire d'upload pour CKEditor
    CKEDITOR_FILE_UPLOADER = "main.upload"
    # Configuration du serveur SMTP pour l'envoi d'emails
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587  # Port pour TLS
    MAIL_USE_TLS = True  # Activation du chiffrement TLS
    # Identifiants de connexion email depuis les variables d'environnement
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")