# Importation des modules nécessaires
from holbydoc import mail  # Instance de Flask-Mail
from flask_mail import Message  # Pour l'envoi d'emails
from flask import url_for  # Pour la génération d'URLs


def send_reset_email(user):
    """Envoie un email de réinitialisation de mot de passe
    
    Args:
        user: L'utilisateur qui a demandé la réinitialisation
        
    Cette fonction génère un token sécurisé et envoie un email
    contenant le lien de réinitialisation à l'utilisateur
    """
    # Génération du token sécurisé
    token = user.get_reset_token()
    # Création du message
    msg = Message(
        "Demande de réinitialisation de mot de passe Pythonic App",
        sender="YOUR EMAIL",
        recipients=[user.email],
        body=f"""Pour réinitialiser votre mot de passe, visitez le lien suivant:
        {url_for('users.reset_password', token=token, _external=True)}
        
        Si vous n'avez pas fait cette demande, ignorez cet email.""",
    )
    # Envoi de l'email
    mail.send(msg)