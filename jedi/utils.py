import os
import secrets

from flask import current_app, url_for
from flask_mail import Message
from PIL import Image

from jedi import mail


def save_picture(
    form_picture, directory="profile_pics", output_size=(125, 125)
):
    random_hex = secrets.token_hex(8)
    _, extension = os.path.splitext(form_picture.filename)
    filename = random_hex + extension
    path = os.path.join(current_app.root_path, "static", directory, filename)

    img = Image.open(form_picture)
    if output_size:
        img.thumbnail(output_size)
    img.save(path)

    return filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "[JEDI] Password reset request",
        sender="noreply@demo.com",
        recipients=[user.email],
    )
    msg.body = f"To reset your password, visit {url_for('reset_token', token=token, _external=True)}"
    mail.send(msg)
