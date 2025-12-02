import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
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


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    role = SelectField(u'Role?:', choices=[('Administrator'), ('Moderator'), ('User')])
    submit = SubmitField('Submit')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    user_all = User.query.all();
    role_all = Role.query.all();
    print(user_all);
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()                        
        if user is None:
            user_role = Role.query.filter_by(name=form.role.data).first();
            user = User(username=form.name.data, role=user_role);
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False),
                           user_all=user_all, role_all = role_all);






#cursos
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

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True, index=True)
    descricao = db.Column(db.String(250), index=True)

class NameForm(FlaskForm):
    name = StringField("Qual é o nome do curso?", validators = [DataRequired()])
    descricao = TextAreaField('Descrição (250 caracteres)', validators = [DataRequired()])
    submit = SubmitField('Cadastrar')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.route('/cursos', methods=['GET','POST'])
def cadastroCursos():
    form = NameForm()
    if form.validate_on_submit():
        curso = Curso.query.filter_by(nome=form.name.data).first()
        if curso is None:
            curso = Curso(nome=form.name.data, descricao=form.descricao.data)
            db.session.add(curso)
            db.session.commit()
        return redirect(url_for('cadastroCursos'))
    cursos = Curso.query.order_by(Curso.nome).all()
    return render_template('cadastroCursos.html', form=form, cursos=cursos)

@app.route('/')
def index():
    return render_template('index.html', current_time = datetime.utcnow())

@app.route('/indisponivel')
def indisponivel():
    return render_template('indisponivel.html', current_time = datetime.utcnow())








#professores
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz # Certifique-se de ter instalado: pip install pytz

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///professores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    disciplina = db.Column(db.String(30), nullable=False)


# ---------------------- INDEX ----------------------
@app.route('/')
def index():
    # Configura o fuso horário (São Paulo)
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso_horario)
    
    # MUDANÇA 1: Formato "Estilo Fabio" (Mês Dia, Ano Hora AM/PM)
    hora_formatada = agora.strftime('%B %d, %Y %I:%M %p')
    
    # MUDANÇA 2: A variável deve se chamar 'hora' para funcionar com {{ hora }} no HTML
    return render_template('index.html', hora=hora_formatada)


# ----------------- PROFESSORES ---------------------
@app.route('/professores', methods=['GET', 'POST'])
def professores():
    if request.method == 'POST':
        nome = request.form['nome']
        disciplina = request.form['disciplina']

        novo = Professor(nome=nome, disciplina=disciplina)
        db.session.add(novo)
        db.session.commit()

        return redirect('/professores')

    todos_professores = Professor.query.all()
    
    # Aqui mantivemos o formato padrão PT-BR para a lista, se preferir
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    hora = datetime.now(fuso_horario).strftime('%d/%m/%Y %H:%M')

    return render_template(
        'professores.html',
        professores=todos_professores,
        hora=hora
    )


# ------------- PÁGINAS NÃO DISPONÍVEIS --------------
@app.route('/disciplinas')
@app.route('/alunos')
@app.route('/cursos')
@app.route('/ocorrencias')
def nao_disponivel():
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    # Usando o formato completo aqui também para ficar bonito
    hora = datetime.now(fuso_horario).strftime('%B %d, %Y %I:%M %p')
    
    # MUDANÇA 3: O template nao_disponivel.html espera 'now', não 'hora'
    return render_template("nao_disponivel.html", now=hora)


if __name__ == '__main__':
    # Garante que as tabelas existam antes de rodar
    with app.app_context():
        db.create_all()
    app.run(debug=True)

