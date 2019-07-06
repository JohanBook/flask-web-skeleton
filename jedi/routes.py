from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os
import secrets
from PIL import Image

from jedi import app, db, bcrypt, forms, mail
from jedi.analyze import formated_analysis
from jedi.models import User

posts = [
    {
        'author': 'JEDI',
        'content': 'This is a project for Johan to learn Flask.'
    },
]


def save_picture(form_picture, directory='profile_pics', output_size=(125, 125)):
    random_hex = secrets.token_hex(8)
    _, extension = os.path.splitext(form_picture.filename)
    filename = random_hex + extension
    path = os.path.join(app.root_path, 'static', directory, filename)

    img = Image.open(form_picture)
    if output_size:
        img.thumbnail(output_size)
    img.save(path)

    return filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        '[JEDI] Password reset request',
        sender='noreply@demo.com',
        recipients=[user.email]
    )
    msg.body = f"To reset your password, visit {url_for('reset_token', token=token, _external=True)}"
    mail.send(msg)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = forms.UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account info has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template(
        'account.html',
        image_file=image_file,
        form=form
    )


@app.route("/analyze", methods=['GET', 'POST'])
@login_required
def analyze():
    form = forms.AnalyzeForm()
    image_data = None
    image_path = None
    if form.picture.data:
        image_path = save_picture(form.picture.data, directory='analyzed', output_size=None)
        image_path = url_for('static', filename='analyzed/' + image_path)
        image_data = formated_analysis(Image.open(form.picture.data))
    return render_template('analyze.html', title='Analyze', form=form, image_data=image_data, image_path=image_path)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logged in as {user.username}', 'success')
            next_page = request.args.get('next')
            return redirect(url_for(next_page)) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email with a reset link has been sent to you', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset pasword', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid url', 'warning')
        return redirect(url_for('reset_request'))
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password

        db.session.commit()
        flash(f'Password have been reset', 'success')
    return render_template('reset_token.html', title='Reset password', form=form)
