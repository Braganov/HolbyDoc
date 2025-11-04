# Importation des modules nécessaires
from flask import Blueprint, request  # Pour créer un blueprint et gérer les requêtes
from holbydoc.models import Lesson, Course  # Modèles de données
from flask import (
    render_template,  # Pour le rendu des templates
)


# Création du blueprint pour les cours
courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/<string:course_title>")
def course(course_title):
    """Affiche un cours spécifique et ses leçons associées
    
    Args:
        course_title: Titre du cours à afficher
        
    Returns:
        Template avec les détails du cours et ses leçons paginées
    """
    # Recherche du cours par son titre
    course = Course.query.filter_by(title=course_title).first()
    course_id = course.id if course else None
    # Récupération du cours ou erreur 404
    course = Course.query.get_or_404(course_id)
    # Pagination des leçons du cours
    page = request.args.get("page", 1, type=int)
    lessons = Lesson.query.filter_by(course_id=course_id).paginate(
        page=page, per_page=6
    )
    return render_template(
        "course.html",
        title=course.title,
        course=course,
        lessons=lessons,
    )


@courses_bp.route("/courses")
def courses():
    """Liste tous les cours disponibles avec pagination"""
    # Pagination des cours
    page = request.args.get("page", 1, type=int)
    courses = Course.query.paginate(page=page, per_page=6)
    return render_template("courses.html", title="Courses", courses=courses)