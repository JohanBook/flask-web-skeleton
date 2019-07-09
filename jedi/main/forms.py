from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, DataRequired
from wtforms import SubmitField


class AnalyzeForm(FlaskForm):
    picture = FileField(
        "Upload image", validators=[FileAllowed(["jpg", "png"]), DataRequired()]
    )
    submit = SubmitField("Analyze")
