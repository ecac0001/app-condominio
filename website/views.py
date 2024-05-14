from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, abort
from flask_login import login_required, current_user
from .models import Ticket, User
from . import db
import json

#define este arquivo como blueprint

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST']) #define a home page (root)
@login_required
def home():
    
    tickets_without_reply = Ticket.query.filter_by(reply_text=None).all()
    
    return render_template('home.html', tickets_without_reply=tickets_without_reply, user=current_user)



#sistema de requisições 

@views.route('/ticket', methods=['GET'])
@login_required
def ticket():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('ticket.html', tickets=tickets, user=current_user)


@views.route('/ticket/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        ticket = Ticket(title=title, description=description, user_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        flash('Solicitação criada com sucesso!', 'success')
        return redirect(url_for('.ticket'))
    return render_template('create_ticket.html', user=current_user)


@views.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Checa se o user atual pode acessar este ticket
    if current_user.id != ticket.user_id:
        abort(403)  # Forbidden se não autorizado
    
    # Obtém as respostas da administração
    administration_reply = ticket.reply_text
    
    if request.method == 'POST':
        ticket.title = request.form['title']
        ticket.description = request.form['description']
        db.session.commit()
        flash('Solicitação atualizada!', 'success')
        return redirect(url_for('.ticket'))
    
    return render_template('view_ticket.html', ticket=ticket, administration_reply=administration_reply, user=current_user)


@views.route('/ticket/<int:ticket_id>/close', methods=['POST'])
@login_required
def close_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Solicitação encerrada!', 'success')
    return redirect(url_for('.ticket'))


@views.route('/admin/tickets-without-reply', methods=['GET', 'POST'])
@login_required
def tickets_without_reply():
    # Checa se u usuário atual é um superuser
    if not current_user.is_superuser:
        return render_template('forbidden.html'), 403

    if request.method == 'POST':
        ticket_id = request.form.get('ticket_id')
        admin_reply_text = request.form.get('admin_reply_text')
        
        # Procura o ticket e atualiza a resposta
        ticket = Ticket.query.get(ticket_id)
        if ticket:
            ticket.reply_text = admin_reply_text
            db.session.commit()
            flash('Resposta enviada!', 'success')

    # Procura todos os tickets com reply_text em valor nulo (null)
    tickets_without_reply = Ticket.query.filter_by(reply_text=None).all()

    # Obtém os tickets
    tickets = Ticket.query.all()
    
    # Associa o ticket ID e o nome do usuário requisitante
    for ticket in tickets:
        user = User.query.get(ticket.user_id)
        if user:
            ticket.primeiro_nome = user.primeiro_nome
        else:
            ticket.primeiro_nome = "Unknown"  # Se não encontrar, retorna erro

    # Associa o ticket ao número do apartamento
    for ticket in tickets:
        user = User.query.get(ticket.user_id)
        ticket.apto = user.apto if user else "Unknown"

    return render_template('tickets_without_reply.html', tickets=tickets_without_reply, user=current_user)