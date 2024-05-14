from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User  # Importa o modelo de usuário
from werkzeug.security import generate_password_hash, check_password_hash  
from . import db  # Importa o objeto de banco de dados
from flask_login import login_user, login_required, current_user, logout_user  

auth = Blueprint('auth', __name__)  

@auth.route('/login', methods=['GET', 'POST'])  # Rota para login
def login():
    if request.method =='POST':  
        email = request.form.get('email')  # Obtém o email do formulário
        password = request.form.get('passwd')  # Obtém a senha do formulário

        user = User.query.filter_by(email=email).first()  # Busca o usuário no banco de dados pelo email
        if user:
            if check_password_hash(user.password, password):  
                flash('Login feito com sucesso!', category='sucess')  # Exibe mensagem de sucesso
                login_user(user, remember=True)  # Realiza o login do usuário
                return redirect(url_for('views.home')) 
            else:
                flash('Senha incorreta, tente novamente.', category='error') 
        else:
            flash('Email não cadastrado.', category='error')  

    return render_template("login.html", user=current_user)

@auth.route('/logout')  
@login_required  # Requer que o usuário esteja logado para acessar essa rota
def logout():
    logout_user()  
    return redirect(url_for('auth.login'))  

@auth.route('/sign-up', methods=['GET', 'POST'])  # Rota para registro de novo usuário
def sign_up():
    if request.method == 'POST':  
        email = request.form.get('email')  #
        primeiroNome = request.form.get('primeiroNome')  
        passwd = request.form.get('passwd')  
        passwd2 = request.form.get('passwd2') 
        apto = request.form.get('apartamento')  
        user = User.query.filter_by(email=email).first()  # Verifica se o email já está cadastrado
        if user:
            flash('Email já cadastrado.', category='error') 
        elif len(email) < 5:
            flash('Email inválido', category='error') 
        elif len(primeiroNome) < 2:
            flash('Nome inválido', category='error')  
        elif passwd != passwd2:
            flash('Senhas estão diferentes!', category='error')  
        elif len(passwd) < 8:
            flash('Senha menor que 8 caracteres', category='error') 
        else:
            novo_user = User(email=email, primeiro_nome=primeiroNome, password=generate_password_hash(passwd, method='pbkdf2:sha256'), apto=apto )  # Cria um novo usuário
            db.session.add(novo_user)  # Adiciona o novo usuário ao banco de dados
            db.session.commit()  # Confirma a transação no banco de dados
            login_user(novo_user, remember=True) 
            flash('Conta criada com sucesso :)', category='success')  # Exibe mensagem de sucesso
            return redirect(url_for('views.home')) 

    return render_template("signup.html", user=current_user) 
