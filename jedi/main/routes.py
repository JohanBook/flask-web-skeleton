from flask import Blueprint, render_template, url_for
from flask_login import login_required
from PIL import Image

from jedi import utils
from jedi.analyze import formated_analysis
from jedi.main import forms

main = Blueprint("main", __name__)

posts = [
    {
        "author": "JEDI",
        "content": "This is a project for Johan to learn Flask.",
    }
]


@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    form = forms.AnalyzeForm()
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
