# Importation des modules nécessaires
from flask import Blueprint  # Pour créer un blueprint Flask
import secrets  # Pour générer des noms de fichiers aléatoires
import os  # Pour la gestion des chemins de fichiers
from holbydoc.models import Lesson, Course  # Modèles de données
from flask_ckeditor import upload_success, upload_fail  # Gestion des uploads CKEditor
from flask import (
    render_template,  # Pour le rendu des templates
    url_for,  # Pour la génération d'URLs
    request,  # Pour accéder aux données de la requête
    send_from_directory,  # Pour servir des fichiers statiques
)
from flask import current_app  # Pour accéder à l'application Flask


# Création du blueprint principal
main = Blueprint("main", __name__)


@main.route("/files/<path:filename>")
def uploaded_files(filename):
    """Sert les fichiers uploadés depuis le dossier media"""
    path = os.path.join(current_app.root_path, "static/media")
    return send_from_directory(path, filename)


@main.route("/upload", methods=["POST"])
def upload():
    """Gère l'upload des images depuis l'éditeur CKEditor
    
    Vérifie l'extension du fichier, génère un nom aléatoire
    et sauvegarde l'image dans le dossier media
    """
    # Récupération du fichier uploadé
    f = request.files.get("upload")
    # Vérification de l'extension
    extension = f.filename.split(".")[-1].lower()
    if extension not in ["jpg", "gif", "png", "jpeg"]:
        return upload_fail(message="File extension not allowed!")
    # Génération d'un nom unique
    random_hex = secrets.token_hex(8)
    image_name = random_hex + extension
    # Sauvegarde du fichier
    f.save(os.path.join(current_app.root_path, "static/media", image_name))
    # Génération de l'URL pour CKEditor
    url = url_for("main.uploaded_files", filename=image_name)
    return upload_success(url, filename=image_name)


@main.route("/")
@main.route("/home")
def home():
    """Page d'accueil
    
    Affiche les 6 dernières leçons et les 6 premiers cours
    """
    # Récupération des leçons triées par date
    lessons = Lesson.query.order_by(Lesson.date_posted.desc()).paginate(
        page=1, per_page=6
    )
    # Récupération des cours
    courses = Course.query.paginate(page=1, per_page=6)
    return render_template("home.html", lessons=lessons, courses=courses)


@main.route("/about")
def about():
    """Page À propos"""
    return render_template("about.html", title="About")