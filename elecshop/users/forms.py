from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from elecshop.models import User
import phonenumbers


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    firstname = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    lastname = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    phone = StringField(
        "Mobile Number", validators=[DataRequired(), Length(min=10, max=13)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(user_name=username.data).first()
        if user:
            raise ValidationError("Username already Exist")

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError("Invalid phone number")
        finally:
            user = User.query.filter_by(contact_num=phone.data).first()
            if user:
                raise ValidationError("Mobile Number Already Registered")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email Already Exist")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    firstname = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    lastname = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.user_name:
            user = User.query.filter_by(user_name=username.data).first()
            if user:
                raise ValidationError("Username Already Exist!")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email Already Exist!")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with this Email. Please Register."
            )


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
