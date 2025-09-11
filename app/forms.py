from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

#Creacion de formularios

#Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')


#Registro
class RegistroForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[('cliente', 'Cliente'), ('motociclista', 'Motociclista')])
    submit = SubmitField('Registrarse')

class SolicitudForm(FlaskForm):
    origen = StringField('Origen', validators=[DataRequired()])
    destino = StringField('Destino', validators=[DataRequired()])
    urgencia = SelectField('Urgencia', choices=[('normal', 'Normal'), ('urgente', 'Urgente'), ('programado', 'Programado')])
    submit = SubmitField('Crear Solicitud')
