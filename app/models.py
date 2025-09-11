from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'cliente' o 'motociclista'

    # Solicitudes hechas por este usuario como cliente
    solicitudes = db.relationship(
        'Solicitud',
        foreign_keys='Solicitud.cliente_id',
        backref='cliente',
        lazy=True
    )

    # Solicitudes asignadas a este usuario como motorizado
    entregas = db.relationship(
        'Solicitud',
        foreign_keys='Solicitud.motorizado_id',
        backref='motociclista',
        lazy=True
    )

class Solicitud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(255))
    destino = db.Column(db.String(255))
    urgencia = db.Column(db.String(20))  # urgente, normal, programado
    cliente_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    motorizado_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    entregado = db.Column(db.Boolean, default=False)
    imagen_entrega = db.Column(db.String(255), nullable=True)