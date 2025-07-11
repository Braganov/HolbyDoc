import secrets
from PIL import Image
import os
from holbydoc.models import User, Lesson, Course
from flask_ckeditor import upload_success, upload_fail
from flask import render_template, url_for, flash, redirect, request, session, abort, send_from_directory
from holbydoc.forms import (
    NewCourseForm,
    NewLessonForm,
    RegistrationForm,
    LoginForm,
    UpdateProfileForm, 
    LessonUpdateForm,
    RequestResetForm,
    ResetPasswordForm,
)
from holbydoc import app, bcrypt, db, mail
from flask_modals import render_template_modal
from flask_mail import Message
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
)


def save_picture(form_picture, path, output_size=None):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, path, picture_name)
    i = Image.open(form_picture)
    if output_size:
        i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name


def get_previous_next_lesson(lesson):
    course = lesson.course_name
    for lsn in course.lessons:
        if lsn.title == lesson.title:
            index = course.lessons.index(lsn)
            previous_lesson = course.lessons[index - 1] if index > 0 else None
            next_lesson = (
                course.lessons[index + 1] if index < len(course.lessons) - 1 else None
            )
            break
    return previous_lesson, next_lesson

def delete_picture(picture_name, path):
    picture_path = os.path.join(app.root_path, path, picture_name)
    try:
        os.remove(picture_path)
    except:
        pass

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Holbydoc App Password Reset Request",
        sender="YOUR EMAIL",
        recipients=[user.email],
        body=f"""To reset your password, visit the following link:
        {url_for('reset_password', token=token, _external=True)}
        
        if you did not make this request, please ignore this email.""",
    )
    mail.send(msg)


@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = os.path.join(app.root_path, 'static/media')
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='File extension not allowed!')
    random_hex = secrets.token_hex(8)
    image_name = random_hex+extension
    f.save(os.path.join(app.root_path, 'static/media', image_name))
    url = url_for('uploaded_files', filename=image_name)
    return upload_success(url, filename=image_name)

@app.route("/")
@app.route("/home")
def home():
    lessons = Lesson.query.order_by(Lesson.date_posted.desc()).paginate(
        page=1, per_page=6
    )
    courses = Course.query.paginate(page=1, per_page=6)
    return render_template("home.html", lessons=lessons, courses=courses)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard", active_tab=None)


@app.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(
                profile_form.picture.data, "static/user_pics", output_size=(150, 150)
            )
            current_user.image_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.bio = profile_form.bio.data
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("profile"))
    elif request.method == "GET":
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


@app.route("/dashboard/new_lesson", methods=["GET", "POST"])
@login_required
def new_lesson():
    new_lesson_form = NewLessonForm()
    new_course_form = NewCourseForm()
    form = ""
    flag = session.pop("flag", False)
    if "content" in request.form:
        form = "new_lesson_form"
    elif "description" in request.form:
        form = "new_course_form"

    if form == "new_lesson_form" and new_lesson_form.validate_on_submit():
        if new_lesson_form.thumbnail.data:
            picture_file = save_picture(
                new_lesson_form.thumbnail.data, "static/lesson_thumbnails"
            )
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
        flash("Your lesson has been created!", "success")
        return redirect(url_for("new_lesson"))

    elif form == "new_course_form" and new_course_form.validate_on_submit():
        if new_course_form.icon.data:
            picture_file = save_picture(
                new_course_form.icon.data, "static/course_icons", output_size=(150, 150)
            )
        course_title = str(new_course_form.title.data).replace(" ", "-")
        course = Course(
            title=course_title,
            description=new_course_form.description.data,
            icon=picture_file,
        )
        db.session.add(course)
        db.session.commit()
        session["flag"] = True
        flash("New Course has been created!", "success")
        return redirect(url_for("dashboard"))

    modal = None if flag else "newCourse"
    return render_template_modal(
        "new_lesson.html",
        title="New Lesson",
        new_lesson_form=new_lesson_form,
        new_course_form=new_course_form,
        active_tab="new_lesson",
        modal=modal,
    )


@app.route("/<string:course>/<string:lesson_slug>")
def lesson(lesson_slug, course):
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


@app.route("/<string:course_title>")
def course(course_title):
    course = Course.query.filter_by(title=course_title).first()
    course_id = course.id if course else None
    course = Course.query.get_or_404(course_id)
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


@app.route("/courses")
def courses():
    page = request.args.get("page", 1, type=int)
    courses = Course.query.paginate(page=page, per_page=6)
    return render_template("courses.html", title="Courses", courses=courses)

@app.route("/dashboard/user_lessons", methods=["GET", "POST"])
@login_required
def user_lessons():
    return render_template(
        "user_lessons.html", title="Your Lessons", active_tab="user_lessons"
    )


@app.route("/<string:course>/<string:lesson_slug>/update", methods=["GET", "POST"])
def update_lesson(lesson_slug, course):
    lesson = Lesson.query.filter_by(slug=lesson_slug).first()
    if lesson:
        previous_lesson, next_lesson = get_previous_next_lesson(lesson)
    lesson_id = lesson.id if lesson else None
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.author != current_user:
        abort(403)
    form = LessonUpdateForm()
    if form.validate_on_submit():
        lesson.course_name = form.course.data
        lesson.title = form.title.data
        lesson.slug = str(form.slug.data).replace(" ", "-")
        lesson.content = form.content.data
        if form.thumbnail.data:
            delete_picture(lesson.thumbnail, "static/lesson_thumbnails")
            new_picture = save_picture(form.thumbnail.data, "static/lesson_thumbnails")
            lesson.thumbnail = new_picture
        db.session.commit()
        flash("Your lesson has been updated!", "success")
        return redirect(
            url_for("lesson", lesson_slug=lesson.slug, course=lesson.course_name.title)
        )
    elif request.method == "GET":
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


@app.route("/lesson/<lesson_id>/delete", methods=["POST"])
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.author != current_user:
        abort(403)
    db.session.delete(lesson)
    db.session.commit()
    flash("Your lesson has been deleted!", "success")
    return redirect(url_for("user_lessons"))

@app.route("/author/<string:username>", methods=["GET"])
def author(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    lessons = (
        Lesson.query.filter_by(author=user)
        .order_by(Lesson.date_posted.desc())
        .paginate(page=page, per_page=6)
    )
    return render_template('author.html', lessons=lessons, user=user)

@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash(
            "If this account exists, you will receive an email with instructions",
            "info",
        )
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("The token is invalid or expired", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated. You can now log in", "success")
        return redirect(url_for("login"))
    return render_template("reset_password.html", title="Reset Password", form=form)