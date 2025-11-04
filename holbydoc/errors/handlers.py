# Importation des modules nécessaires
from flask import Blueprint, render_template  # Pour créer un blueprint et rendre les templates

# Création du blueprint pour la gestion des erreurs
errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """Gère les erreurs 404 (Page non trouvée)"""
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """Gère les erreurs 403 (Accès interdit)"""
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """Gère les erreurs 500 (Erreur serveur interne)"""
    return render_template('errors/500.html'), 500