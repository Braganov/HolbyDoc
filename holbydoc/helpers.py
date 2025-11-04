# Importation des modules nécessaires
import secrets  # Pour la génération de noms de fichiers aléatoires
import os  # Pour la manipulation des chemins de fichiers
from PIL import Image  # Pour le traitement d'images
from flask import current_app  # Pour accéder à l'application Flask

def save_picture(form_picture, path, output_size=None):
    """Sauvegarde une image téléchargée avec un nom aléatoire
    
    Args:
        form_picture: L'objet fichier uploadé depuis le formulaire
        path: Le chemin où sauvegarder l'image
        output_size: Tuple (largeur, hauteur) pour redimensionner l'image
        
    Returns:
        str: Le nom du fichier généré
    """
    # Génération d'un nom de fichier aléatoire
    random_hex = secrets.token_hex(8)
    # Récupération de l'extension du fichier original
    _, f_ext = os.path.splitext(form_picture.filename)
    # Création du nouveau nom de fichier
    picture_name = random_hex + f_ext
    # Construction du chemin complet
    picture_path = os.path.join(current_app.root_path, path, picture_name)
    # Ouverture et traitement de l'image
    i = Image.open(form_picture)
    # Redimensionnement si une taille est spécifiée
    if output_size:
        i.thumbnail(output_size)
    # Sauvegarde de l'image
    i.save(picture_path)
    # Retour du nom du fichier
    return picture_name