from flask import Blueprint, render_template, url_for, flash, redirect, abort
from flask_login import login_required, current_user
from PIL import Image

from jedi import db, utils
from jedi.analyze import formated_analysis
from jedi.main import forms
from jedi.models import Purchase

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
        if current_user.check_credit(1):
            current_user.withdraw_credit(1)
            address = utils.random_hex()
            image_file = utils.save_picture(
                form.picture.data, directory="analyzed", output_size=None, hex=address
            )
            purchase = Purchase(address=address, owner=current_user, image_file=image_file)
            db.session.add(purchase)
            db.session.commit()

            return redirect(url_for('main.view_order', order=purchase.address))
        else:
            flash('Your credit is too low. Please get more to use this functionality', 'danger')
            return redirect(url_for('main.analyze'))

    return render_template(
        "analyze.html",
        title="Analyze",
        form=form
    )


@main.route("/analyze/<order>", methods=["GET", "POST"])
@login_required
def view_order(order):
    purchase = Purchase.query.filter_by(address=order).first()
    if purchase and purchase.owner == current_user:
        image_file = url_for(
            "static", filename="analyzed/" + purchase.image_file
        )
        return render_template('order.html', purchase=purchase, image_file=image_file, image_data={})
    else:
        abort(404)


@main.route("/credits")
@login_required
def credits():
    return render_template('credits.html')
