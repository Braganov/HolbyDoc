# Importation des modules nécessaires
from flask import Blueprint  # Pour créer un blueprint Flask
from holbydoc.models import User, Lesson  # Modèles de données
from flask import (
    render_template,  # Pour le rendu des templates
    url_for,  # Pour la génération d'URLs
    flash,  # Pour les messages flash
    redirect,  # Pour les redirections
    request,  # Pour accéder aux données de la requête
)
from holbydoc.users.forms import (  # Formulaires utilisateur
    RegistrationForm,  # Inscription
    LoginForm,  # Connexion
    UpdateProfileForm,  # Mise à jour du profil
    RequestResetForm,  # Demande de réinitialisation
    ResetPasswordForm,  # Réinitialisation du mot de passe
)
from holbydoc import bcrypt, db  # Instances de l'application
from flask_login import (  # Gestion de l'authentification
    login_required,  # Décorateur pour routes protégées
    login_user,  # Connexion utilisateur
    current_user,  # Utilisateur actuel
    logout_user,  # Déconnexion utilisateur
)
from holbydoc.helpers import save_picture  # Utilitaire de sauvegarde d'images
from holbydoc.users.helpers import send_reset_email  # Envoi d'email de réinitialisation

# Création du blueprint pour les utilisateurs
users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    """Gère l'inscription d'un nouvel utilisateur"""
    # Redirection si déjà connecté
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hachage du mot de passe
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        # Création du nouvel utilisateur
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Compte créé avec succès pour {form.username.data}", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    """Gère la connexion d'un utilisateur"""
    # Redirection si déjà connecté
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        # Vérification des identifiants
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Vous êtes maintenant connecté !", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Échec de la connexion. Vérifiez vos identifiants", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    """Déconnecte l'utilisateur actuel"""
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """Affiche le tableau de bord de l'utilisateur"""
    return render_template("dashboard.html", title="Dashboard", active_tab=None)


@users.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Gère la mise à jour du profil utilisateur"""
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        # Traitement de la photo de profil
        if profile_form.picture.data:
            picture_file = save_picture(
                profile_form.picture.data, "static/user_pics", output=(150, 150)
            )
            current_user.image_file = picture_file
        # Mise à jour des informations
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.bio = profile_form.bio.data
        db.session.commit()
        flash("Votre profil a été mis à jour", "success")
        return redirect(url_for("users.profile"))
    elif request.method == "GET":
        # Pré-remplissage du formulaire
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio
    image_file = url_for("static", filename=f"user_pics/{current_user.image_file}")
    return render_template(
        "profile.html",
        title="Profile",
        profile_form=profile_form,
        image_file=image_file,
        active_tab="profile",
    )


@users.route("/author/<string:username>", methods=["GET"])
def author(username):
    """Affiche le profil public d'un auteur et ses leçons"""
    # Récupération de l'auteur
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    # Récupération des leçons de l'auteur
    lessons = (
        Lesson.query.filter_by(author=user)
        .order_by(Lesson.date_posted.desc())
        .paginate(page=page, per_page=6)
    )
    return render_template("author.html", lessons=lessons, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    """Gère les demandes de réinitialisation de mot de passe"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash(
            "Si ce compte existe, vous recevrez un email avec les instructions",
            "info",
        )
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Traite la réinitialisation du mot de passe avec le token"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("Le token est invalide ou expiré", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Hachage et mise à jour du nouveau mot de passe
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(f"Votre mot de passe a été mis à jour. Vous pouvez maintenant vous connecter", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_password.html", title="Reset Password", form=form)