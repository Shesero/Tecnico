from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import db
from app.forms import LoginForm, RegistroForm
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

# Todo Desarrollo de authentificacion

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            flash("Credenciales incorrectas", "danger")
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('dashboard.dashboard_home'))
    return render_template("login.html", form=form)

@auth.route('/registro', methods=['GET','POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email ya registrado", "danger")
            return redirect(url_for('auth.registro'))
        hash_pass = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hash_pass, role=form.role.data)
        db.session.add(user)  
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard.dashboard_home'))
    return render_template("registro.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))