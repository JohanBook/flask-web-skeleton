from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flask_web_skeleton import db, utils
from flask_web_skeleton.models import Purchase, User
from flask_web_skeleton.users import forms

users = Blueprint("users", __name__)


# Attackers will be able to modify the tokens, so don't store the user account information or timeout information
# in them. They should be an unpredictable random binary blob used only to identify a record in a database table


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
        flash(
            "Your email is not confirmed. Please confirm it to use flask_web_skeleton services",
            "warning",
        )
    return render_template(
        "account.html", image_file=image_file, form=form, purchases=purchases
    )


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            user.login()
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
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account successfully created for {form.username.data}", "success"
        )

        login_user(user)  # also login in database
        return redirect(url_for("main.home"))
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
        "reset_request.html", title="Reset password", form=form
    )


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    user = User.verify_password_reset(token)
    if user is None:
        flash("Invalid url", "warning")
        return redirect(url_for("users.reset_request"))

    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        flash(f"Password have been reset", "success")
        return redirect(url_for("main.home"))

    return render_template(
        "reset_token.html", title="Reset password", form=form
    )


@users.route("/user/<username>")
@login_required
def user(username):
    return render_template("reset_request.html")
