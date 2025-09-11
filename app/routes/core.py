from flask import Blueprint, redirect, url_for
from flask_login import current_user

core = Blueprint('core', __name__)

# Ruta principal
@core.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_home'))
    return redirect(url_for('auth.login'))
