# Importation des modules nécessaires
from flask import Blueprint  # Pour créer un blueprint Flask
from holbydoc.models import Lesson, Course  # Modèles de données
from flask import (
    render_template,  # Pour le rendu des templates
    url_for,  # Pour la génération d'URLs
    flash,  # Pour les messages flash
    redirect,  # Pour les redirections
    request,  # Pour accéder aux données de la requête
    session,  # Pour la session utilisateur
    abort,  # Pour les erreurs HTTP
)
from holbydoc.lessons.forms import (  # Formulaires pour les leçons
    NewLessonForm,  # Création de leçon
    LessonUpdateForm,  # Mise à jour de leçon
)
from holbydoc.courses.forms import NewCourseForm  # Formulaire pour nouveau cours

from holbydoc import db  # Instance de la base de données
from flask_modals import render_template_modal  # Pour les fenêtres modales
from flask_login import (  # Gestion de l'authentification
    login_required,  # Protection des routes
    current_user,  # Utilisateur actuel
)
from holbydoc.helpers import save_picture  # Utilitaire pour sauvegarder les images
from holbydoc.lessons.helpers import get_previous_next_lesson, delete_picture  # Helpers spécifiques aux leçons

# Création du blueprint pour les leçons
lessons = Blueprint("lessons", __name__)


@lessons.route("/dashboard/new_lesson", methods=["GET", "POST"])
@login_required
def new_lesson():
    """Gère la création d'une nouvelle leçon et d'un nouveau cours
    
    Cette route permet soit de créer une nouvelle leçon,
    soit de créer un nouveau cours via une fenêtre modale
    """
    new_lesson_form = NewLessonForm()
    new_course_form = NewCourseForm()
    form = ""
    flag = session.pop("flag", False)
    # Détermination du formulaire soumis
    if "content" in request.form:
        form = "new_lesson_form"
    elif "description" in request.form:
        form = "new_course_form"

    if form == "new_lesson_form" and new_lesson_form.validate_on_submit():
        # Traitement de la miniature
        if new_lesson_form.thumbnail.data:
            picture_file = save_picture(
                new_lesson_form.thumbnail.data, "static/lesson_thumbnails"
            )
        # Création de la leçon
        lesson_slug = str(new_lesson_form.slug.data).replace(" ", "-")
        course = new_lesson_form.course.data
        lesson = Lesson(
            title=new_lesson_form.title.data,
            content=new_lesson_form.content.data,
            slug=lesson_slug,
            author=current_user,
            course_name=course,
            thumbnail=picture_file,
        )
        db.session.add(lesson)
        db.session.commit()
        flash("Votre leçon a été créée !", "success")
        return redirect(url_for("lessons.new_lesson"))

    elif form == "new_course_form" and new_course_form.validate_on_submit():
        # Traitement de l'icône du cours
        if new_course_form.icon.data:
            picture_file = save_picture(
                new_course_form.icon.data, "static/course_icons", output_size=(150, 150)
            )
        # Création du cours
        course_title = str(new_course_form.title.data).replace(" ", "-")
        course = Course(
            title=new_course_form.title.data,
            description=new_course_form.description.data,
            icon=picture_file,
        )
        db.session.add(course)
        db.session.commit()
        session["flag"] = True
        flash("Le nouveau cours a été créé !", "success")
        return redirect(url_for("users.dashboard"))

    modal = None if flag else "newCourse"
    return render_template_modal(
        "new_lesson.html",
        title="New Lesson",
        new_lesson_form=new_lesson_form,
        new_course_form=new_course_form,
        active_tab="new_lesson",
        modal=modal,
    )


@lessons.route("/<string:course>/<string:lesson_slug>")
def lesson(lesson_slug, course):
    """Affiche une leçon spécifique avec navigation précédent/suivant"""
    # Récupération de la leçon et de la navigation
    lesson = Lesson.query.filter_by(slug=lesson_slug).first()
    if lesson:
        previous_lesson, next_lesson = get_previous_next_lesson(lesson)
    lesson_id = lesson.id if lesson else None
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template(
        "lesson_view.html",
        title=lesson.title,
        lesson=lesson,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
    )


@lessons.route("/dashboard/user_lessons", methods=["GET", "POST"])
@login_required
def user_lessons():
    """Affiche la liste des leçons de l'utilisateur"""
    return render_template(
        "user_lessons.html", title="Your Lessons", active_tab="user_lessons"
    )


@lessons.route("/<string:course>/<string:lesson_slug>/update", methods=["GET", "POST"])
def update_lesson(lesson_slug, course):
    """Gère la mise à jour d'une leçon existante"""
    # Récupération de la leçon
    lesson = Lesson.query.filter_by(slug=lesson_slug).first()
    if lesson:
        previous_lesson, next_lesson = get_previous_next_lesson(lesson)
    lesson_id = lesson.id if lesson else None
    lesson = Lesson.query.get_or_404(lesson_id)
    # Vérification des droits d'accès
    if lesson.author != current_user:
        abort(403)
    form = LessonUpdateForm()
    if form.validate_on_submit():
        # Mise à jour des informations
        lesson.course_name = form.course.data
        lesson.title = form.title.data
        lesson.slug = str(form.slug.data).replace(" ", "-")
        lesson.content = form.content.data
        # Traitement de la nouvelle miniature
        if form.thumbnail.data:
            delete_picture(lesson.thumbnail, "static/lesson_thumbnails")
            new_picture = save_picture(form.thumbnail.data, "static/lesson_thumbnails")
            lesson.thumbnail = new_picture
        db.session.commit()
        flash("Votre leçon a été mise à jour !", "success")
        return redirect(
            url_for("lessons.lesson", lesson_slug=lesson.slug, course=lesson.course_name.title)
        )
    elif request.method == "GET":
        # Pré-remplissage du formulaire
        form.course.data = lesson.course_name.title
        form.title.data = lesson.title
        form.slug.data = lesson.slug
        form.content.data = lesson.content
    return render_template(
        "update_lesson.html",
        title="Update | " + lesson.title,
        lesson=lesson,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
        form=form,
    )


@lessons.route("/lesson/<lesson_id>/delete", methods=["POST"])
def delete_lesson(lesson_id):
    """Supprime une leçon"""
    # Récupération de la leçon
    lesson = Lesson.query.get_or_404(lesson_id)
    # Vérification des droits d'accès
    if lesson.author != current_user:
        abort(403)
    # Suppression de la leçon
    db.session.delete(lesson)
    db.session.commit()
    flash("Votre leçon a été supprimée !", "success")
    return redirect(url_for("lessons.user_lessons"))