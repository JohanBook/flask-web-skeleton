from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from PIL import Image

from jedi import utils
from jedi.analyze import formated_analysis
from jedi.main import forms

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html")


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    form = forms.AnalyzeForm()
    if form.validate_on_submit():
        print('Detected submit')
        if current_user.check_credit(1):
            current_user.withdraw_credit(1)
            print('Withdrawn credit')
        else:
            flash('Your credit is too low. Please get more to use this functionality', 'danger')
            return redirect(url_for('main.analyze'))

    image_data = None
    image_path = None
    if form.picture.data:
        image_path = utils.save_picture(
            form.picture.data, directory="analyzed", output_size=None
        )
        image_path = url_for("static", filename="analyzed/" + image_path)
        image_data = formated_analysis(Image.open(form.picture.data))
    return render_template(
        "analyze.html",
        title="Analyze",
        form=form,
        image_data=image_data,
        image_path=image_path,
    )


@main.route("/credits")
@login_required
def credits():
    return render_template('credits.html')
