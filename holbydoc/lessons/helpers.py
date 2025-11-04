# Importation des modules nécessaires
import os  # Pour la manipulation des fichiers
from flask import current_app  # Pour accéder à l'application Flask


def get_previous_next_lesson(lesson):
    """Récupère les leçons précédente et suivante dans un cours
    
    Args:
        lesson: La leçon actuelle
        
    Returns:
        tuple: (leçon_précédente, leçon_suivante)
        Chaque élément peut être None s'il n'y a pas de leçon
        précédente ou suivante
    """
    # Récupération du cours parent
    course = lesson.course_name
    # Recherche de la position de la leçon dans le cours
    for lsn in course.lessons:
        if lsn.title == lesson.title:
            index = course.lessons.index(lsn)
            # Détermination des leçons adjacentes
            previous_lesson = course.lessons[index - 1] if index > 0 else None
            next_lesson = (
                course.lessons[index + 1] if index < len(course.lessons) - 1 else None
            )
            break
    return previous_lesson, next_lesson


def delete_picture(picture_name, path):
    """Supprime une image du système de fichiers
    
    Args:
        picture_name: Nom du fichier image
        path: Chemin relatif vers le dossier contenant l'image
        
    La fonction ignore silencieusement les erreurs (fichier inexistant, etc.)
    """
    # Construction du chemin complet
    picture_path = os.path.join(current_app.root_path, path, picture_name)
    # Tentative de suppression
    try:
        os.remove(picture_path)
    except:
        pass  # Ignore les erreurs de suppression