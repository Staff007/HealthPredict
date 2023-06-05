from app.models import User
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", render_kw={"placeholder": "Имя"}, validators=[DataRequired()]
    )

    email = EmailField(
        "Email",
        render_kw={"placeholder": "Электронная почта"},
        validators=[DataRequired(), Email()],
    )

    password = PasswordField(
        "Password", render_kw={"placeholder": "Пароль"}, validators=[DataRequired()]
    )

    repeat_password = PasswordField(
        "Repeat Password",
        render_kw={"placeholder": "Повторите пароль"},
        validators=[DataRequired(), EqualTo("password")],
    )

    submit = SubmitField("Зарегестрироваться")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Кажется, такой email уже зарегистрирован")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        render_kw={"placeholder": "Введите адрес электронной почты"},
        validators=[DataRequired()],
    )

    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Введите пароль"},
        validators=[DataRequired()],
    )

    submit = SubmitField("Войти")
