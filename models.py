from app import db

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    disciplina = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Professor {self.nome}>'
