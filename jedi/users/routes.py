from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from jedi import bcrypt, db, utils
from jedi.models import User, Purchase
from jedi.users import forms

users = Blueprint("users", __name__)


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = forms.UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = utils.save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account info has been updated", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file
    )
    purchases = Purchase.query.all()
    if not current_user.confirmed_email:
        flash('Your email is not confirmed. Please confirm it to use JEDI services', 'warning')
    return render_template("account.html", image_file=image_file, form=form, purchases=purchases)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user, remember=form.remember.data)
            flash(f"Logged in as {user.username}", "success")
            next_page = request.args.get("next")
            return (
                redirect(url_for(next_page))
                if next_page
                else redirect(url_for("main.home"))
            )
        else:
            flash(f"Login unsuccessful", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account successfully created for {form.username.data}", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = forms.RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        utils.send_reset_email(user)
        flash("An email with a reset link has been sent to you", "info")
        return redirect(url_for("users.login"))
    return render_template(
        "reset_request.html", title="Reset pasword", form=form
    )


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid url", "warning")
        return redirect(url_for("users.reset_request"))
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")
        user.password = hashed_password

        db.session.commit()
        flash(f"Password have been reset", "success")
    return render_template(
        "reset_token.html", title="Reset password", form=form
    )
