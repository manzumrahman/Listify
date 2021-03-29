from flask import Blueprint, render_template, request, flash, redirect
from .models import User
from . import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already exists. Login to continue", 'warning')
        elif len(email) <= 4:
            flash('Email Address Must Be Greater than 4 characters', category='danger')
        elif len(name) < 3:
            flash('First Name Must Be Greater than 4 characters', category='danger')
        elif len(password1) < 4:
            flash('Password Must Be Greater than or equal to 4 characters', category='danger')
        elif password1 != password2:
            flash("Passwords doesn't match", category='danger')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created Successfully', category='success')
            login_user(new_user, remember=True)
            return redirect('/app')
    return render_template('signup.html', user=current_user)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!", 'success')
                login_user(user, remember=True)
                return redirect('/')
            else:
                flash("Wrong Password, Try again.", 'danger')
        else:
            flash("Email doesn't exist", 'danger')
    return render_template('login.html', user=current_user)


@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/login')


