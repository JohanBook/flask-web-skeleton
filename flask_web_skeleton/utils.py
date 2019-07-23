import os
import secrets

from flask import current_app, url_for
from flask_mail import Message
from PIL import Image

from flask_web_skeleton import mail


def random_hex(length=8):
    return secrets.token_hex(length)


def get_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension


def save_picture(
    form_picture, directory="profile_pics", output_size=(125, 125), hex=None
):
    if not hex:
        hex = secrets.token_hex(8)
    extension = get_extension(form_picture.filename)
    filename = hex + extension
    path = os.path.join(current_app.root_path, "static", directory, filename)

    img = Image.open(form_picture)
    if output_size:
        img.thumbnail(output_size)
    img.save(path)

    return filename


def send_reset_email(user):
    token = user.password_reset_request()
    msg = Message(
        "[flask_web_skeleton] Password reset request",
        sender="noreply@demo.com",
        recipients=[user.email],
    )
    msg.body = f"To reset your password, visit {url_for('users.reset_token', token=token, _external=True)}"
    print(msg.body)
    # mail.send(msg)
