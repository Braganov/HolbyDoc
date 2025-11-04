# Importation des modules nécessaires pour l'interface d'administration
from flask import Blueprint  # Pour créer un blueprint Flask
from flask_admin.contrib.sqla import ModelView  # Vue de base pour l'admin
from flask_login import current_user  # Utilisateur connecté
from holbydoc import admin, db, bcrypt  # Instances de l'application
from holbydoc.models import User, Lesson, Course  # Modèles de données
from flask_admin import AdminIndexView  # Vue index de l'admin

# Création du blueprint pour l'administration
adminbp = Blueprint("adminbp", __name__)


class UserModelView(ModelView):
    """Vue personnalisée pour la gestion des utilisateurs dans l'admin"""
    
    def on_model_change(self, form, model, is_created):
        """Hachage du mot de passe lors de la création/modification d'un utilisateur"""
        model.password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8)"
        )

    def is_accessible(self):
        """Vérifie si l'utilisateur a accès à cette vue (admin uniquement)"""
        return current_user.is_authenticated and current_user.id == 1


class MyModelView(ModelView):
    """Vue de base pour les autres modèles dans l'admin"""
    
    def is_accessible(self):
        """Vérifie si l'utilisateur a accès à cette vue (admin uniquement)"""
        return current_user.is_authenticated and current_user.id == 1


class MyAdminIndexView(AdminIndexView):
    """Vue personnalisée pour la page d'accueil de l'admin"""
    
    def is_accessible(self):
        """Vérifie si l'utilisateur a accès à l'interface admin"""
        return current_user.is_authenticated and current_user.id == 1


# Enregistrement des vues dans l'interface d'administration
admin.add_view(UserModelView(User, db.session))  # Vue pour gérer les utilisateurs
admin.add_view(MyModelView(Lesson, db.session))  # Vue pour gérer les leçons
admin.add_view(MyModelView(Course, db.session))  # Vue pour gérer les cours