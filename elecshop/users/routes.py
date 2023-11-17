from elecshop import db, bcrypt
from flask import render_template, url_for, flash, redirect, request, Blueprint
from elecshop.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from elecshop.users.utils import save_picture, send_reset_email
from elecshop.models import User
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("shop.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            user_name=form.username.data,
            first_name=form.firstname.data,
            last_name=form.lastname.data,
            contact_num=form.phone.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()

        flash(f"Account Created For {form.firstname.data} !", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("shop.home"))

    form = LoginForm()
    if form.validate_on_submit():
        # user_1 = User.query.filter_by(user_name = form.uname_email_phone.data).first()
        # user_2 = User.query.filter_by(email = form.uname_email_phone.data).first()
        # user_3 = User.query.filter_by(contact_num = form.uname_email_phone.data).first()
        # user = next(usr for usr in [user_1, user_2, user_3] if usr)
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            flash(f"You have been logged in: {user.user_name} !", "success")
            return redirect(url_for("shop.home"))
        else:
            flash(f"Login Unsuccessful!", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("shop.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.user_name = form.username.data
        current_user.first_name = form.firstname.data
        current_user.last_name = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Account Updated Successfully", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.user_name
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name
        form.email.data = current_user.email

    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("shop.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Email with reset password link has been sent.", "success")
        return redirect(url_for("users.login"))
    return render_template(
        "reset_request.html", title="Request Reset Password", form=form
    )


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("shop.home"))

    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid or Expire Token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
