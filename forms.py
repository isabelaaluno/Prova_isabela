from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ProfessorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    disciplina = SelectField('Disciplina', choices=[
        ('DSWA5', 'DSWA5'),
        ('GPSA5', 'GPSA5'),
        ('GITP5', 'GITP5')
    ], validators=[DataRequired()])
    submit = SubmitField('Cadastrar')
