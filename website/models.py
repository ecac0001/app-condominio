from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    primeiro_nome = db.Column(db.String(150))
    is_superuser = db.Column(db.Boolean, default=False)
    apto = db.Column(db.String(10))
    info = db.Column(db.Text, nullable=True)
    info_posted = db.Column(db.DateTime, default=func.now(), nullable=True)  # Adicionando coluna para armazenar a data e hora da postagem

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tickets', lazy=True))
    reply_text = db.Column(db.Text, nullable=True) 

    def __repr__(self):
        return f'<Ticket {self.id}>'
