from atatek.db import db, Tickets, EditTicket, AddTicket, Tree
from sqlalchemy.exc import IntegrityError
from atatek.utils import get_tree_data_on_request

def create_ticket_crud(type: str, created_by: int):
    ticket = Tickets(type=type, created_by=created_by)
    db.session.add(ticket)
    db.session.commit()
    return ticket

def add_create_ticket(ticket: id, parend: id, name: str):
    add_ticket = AddTicket(ticket=ticket, parent=parend, name=name)
    db.session.add(add_ticket)
    db.session.commit()
    return add_ticket

def edit_ticket_crud(ticket: int, tree: int, name: str, birth: int, death: int, biography: str):
    edit_ticket = EditTicket(
        ticket=ticket,
        tree=tree,
        name=name,
        birth=birth,
        death=death,
        biography=biography
    )
    db.session.add(edit_ticket)
    db.session.commit()
    return edit_ticket

def status_changer(ticket: int, is_active: None, is_cancelled: None, is_confirmed: None):
    ticket = Tickets.query.filter_by(id=ticket).first()
    if ticket:
        # Устанавливаем статус
        if is_active:
            ticket.is_active = True
            ticket.is_cancelled = False
            ticket.is_confirmed = False
        elif is_cancelled:
            ticket.is_active = False
            ticket.is_cancelled = True
            ticket.is_confirmed = False
        elif is_confirmed:
            ticket.is_active = False
            ticket.is_cancelled = False
            ticket.is_confirmed = True
        # Сохраняем изменения
        db.session.commit()
        return True
    else:
        return False

def get_user_tickets_all(user):
    tickets = Tickets.query.filter_by(created_by=user).all()
    return tickets

def get_user_ticket_by_id(id):
    ticket = Tickets.query.filter_by(id=id).first()
    details = []
    if ticket.type == 'add':
        ticketdetails = AddTicket.query.filter_by(ticket=ticket.id).all()
        for ticketbum in ticketdetails:
            parent = Tree.query.filter_by(id=ticketbum.parent).first()
            details.append({
                'id': ticketbum.id,
                'name': ticketbum.name,
                'parent': parent.name,
            })
        response = {
            "id": ticket.id,
            "type": ticket.type,
            "is_active": ticket.is_active,
            "is_cancelled": ticket.is_cancelled,
            "is_confirmed": ticket.is_confirmed,
            "created_at": ticket.created_at,
            "created_by": ticket.created_by,
            "details": details,
        }
        return response

    elif ticket.type == 'edit':
        ticketdetails = EditTicket.query.filter_by(ticket=ticket.id).all()
        for ticketbum in ticketdetails:
            details.append({
                'id': ticketbum.id,
                'name': ticketbum.name,
                'birth': ticketbum.birth if ticketbum.birth is not None else "Көрсетілмеген",
                'death': ticketbum.death if ticketbum.birth is not None else "Көрсетілмеген",
                'biography': ticketbum.biography,
            })

        response = {
            "id": ticket.id,
            "type": ticket.type,
            "is_active": ticket.is_active,
            "is_cancelled": ticket.is_cancelled,
            "is_confirmed": ticket.is_confirmed,
            "created_at": ticket.created_at,
            "created_by": ticket.created_by,
            "details": details,
        }
        return response
