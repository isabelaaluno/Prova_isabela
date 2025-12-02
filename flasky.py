
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import request
from flask import make_response
from flask import redirect, url_for, flash, session
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = "Chave forte"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True, index=True)
    disciplina = db.Column(db.Colum(db.String(64),db.ForeignKey(disciplina.nome))

    def __repr__(self):
        return '<Aluno %r>' % self.nome

class AlunoForm(FlaskForm):
    name = StringField("Cadastre o novo Aluno:", validators = [DataRequired()])
    DISCIPLINA_CHOICES = [
        ('DSWA5', 'DSWA5'),
        ('TCOA5', 'TCOA5'),
        ('PJIA5', 'PJIA5'),
        ('SODA5', 'SODA5'),
        ('BDD01', 'BDD01'),
        ('SEGI7', 'SEGI7'),
    ]
    disciplina = SelectField(u'Disciplina associada:', coerce=DISCIPLINA_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Aluno=Aluno, Disciplina=Disciplina)

@app.route('/')
def index():
    return render_template('index.html', current_time = datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', current_time=datetime.utcnow()), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/indisponivel')
def indisponivel():
    return render_template('indisponivel.html', current_time = datetime.utcnow())

@app.route('/alunos', methods=['GET', 'POST'])
def cadastro_alunos():
    form = AlunoForm()
    alunos_all = Aluno.query.order_by(Aluno.nome).all();
    print(alunos_all);
    if form.validate_on_submit():
        aluno = Aluno.query.filter_by(nome=form.name.data).first()
        if aluno is None:
            aluno_disc = Disc.query.filter_by(name=form.disc.data).first();
            aluno = Aluno(nome=form.name.data, disc_name=aluno_disc);
            db.session.add(aluno)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form,
                           alunos_all=alunos_all);
