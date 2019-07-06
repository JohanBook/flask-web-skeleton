from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from jedi.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(
        'Sign up'
    )

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError(
                f'Username already taken'
            )

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError(
                f'Email already in use'
            )


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    remember = BooleanField(
        'Remember me'
    )
    submit = SubmitField(
        'Login'
    )


class UpdateAccount(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    picture = FileField(
        'Update profile picture',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    submit = SubmitField(
        'Update'
    )

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError(
                    f'Username already taken'
            )

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError(
                    f'Email already in use'
                )


class AnalyzeForm(FlaskForm):
    picture = FileField(
        'Upload image',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    submit = SubmitField(
        'Analyze'
    )


class RequestResetForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField(
        'Request password reset'
    )

    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError(
                f'Email not found'
            )


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(
        'Reset password'
    )

