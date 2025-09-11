from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Solicitud, db
from app.forms import SolicitudForm

dashboard = Blueprint('dashboard', __name__)

# Todo Desarrollo Del Panel De Control

@dashboard.route('/dashboard')
@login_required
def dashboard_home():
    if current_user.role == 'cliente':
        solicitudes = Solicitud.query.filter_by(cliente_id=current_user.id).all()
    else:
        solicitudes = Solicitud.query.all()
    return render_template("dashboard.html", solicitudes=solicitudes, current_user=current_user)

@dashboard.route('/nueva_solicitud', methods=["GET", "POST"])
@login_required
def nueva_solicitud():
    form = SolicitudForm()
    if form.validate_on_submit():
        nueva_solicitud = Solicitud(
            origen=form.origen.data,
            destino=form.destino.data,
            urgencia=form.urgencia.data,
            cliente_id=current_user.id
        )
        db.session.add(nueva_solicitud)
        db.session.commit()
        flash("Solicitud creada exitosamente", "success")
        return redirect(url_for('dashboard.dashboard_home'))
    return render_template("nueva_solicitud.html", form=form)

@dashboard.route('/eliminar_solicitud/<int:solicitud_id>', methods=["POST", "GET"])
@login_required
def eliminar_solicitud(solicitud_id):
    solicitud = Solicitud.query.get(solicitud_id)
    if not solicitud:
        flash("Solicitud no encontrada", "danger")
        return redirect(url_for('dashboard'))
    if solicitud.cliente_id != current_user.id:
        flash("No tienes permiso para eliminar esta solicitud", "danger")
        return redirect(url_for('dashboard'))
    db.session.delete(solicitud)
    db.session.commit()
    flash("Solicitud eliminada exitosamente", "success")
    return redirect(url_for('dashboard.dashboard_home'))

@dashboard.route('/aceptar_solicitud/<int:solicitud_id>', methods=["POST", "GET"])
@login_required
def aceptar_solicitud(solicitud_id):
    solicitud = Solicitud.query.get(solicitud_id)
    solicitud.motorizado_id = current_user.id
    solicitud.entregado = True
    solicitud.imagen_entrega = "Firma Digital"
    db.session.commit()
    flash("Solicitud aceptada exitosamente", "success")
    return redirect(url_for('dashboard.dashboard_home'))

@dashboard.route('/ver_detalles/<int:solicitud_id>', methods=["GET"])
@login_required
def ver_detalles(solicitud_id):
    solicitud = Solicitud.query.get(solicitud_id)
    if not solicitud:
        flash("Solicitud no encontrada", "danger")
        return redirect(url_for('dashboard.dashboard_home'))
    return render_template("ver_detalles.html", solicitud=solicitud)