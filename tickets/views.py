from django.shortcuts import render, redirect
from .models import Ticket, Response
from .forms import ValidateResponse, ValidateTicket
from django.http import HttpResponseNotFound

SERVER_NAME = 'Example server'


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = ValidateTicket(request.POST)
        if form.is_valid():
            ticket = Ticket.objects.create(user=request.user, title=request.POST['title'], problem=request.POST['text'])
            return redirect('/tickets/id/' + str(ticket.id))
    tickets = Ticket.objects.filter(user=request.user)
    if not request.user.is_staff:
        context = {
            'ticket_quantity': tickets.count(),
            'tickets': tickets,
            'user': request.user,
            'SERVER_NAME': SERVER_NAME,
            'Title': 'Tickets',
        }
    else:
        user_tickets = Ticket.objects.all()
        context = {
            'ticket_quantity': tickets.count(),
            'tickets': tickets,
            'user_tickets': user_tickets,
            'user': request.user,
            'SERVER_NAME': SERVER_NAME,
            'Title': 'Tickets',
        }
    return render(request, 'Tickets/tickets.html', context)


def ticket_close(request, ticket_id):
    if not request.user.is_authenticated:
        return redirect('/')
    tickets = Ticket.objects.filter(id=ticket_id)
    if tickets.count() != 0:
        if tickets.first().user == request.user or request.user.is_staff:
            tickets = Ticket.objects.filter(id=ticket_id).first()
            tickets.solved = True
            tickets.save()
            if request.user.is_staff:
                Response.objects.create(user=request.user, text='<strong>Closed by administrator. If you have any'
                                                                ' question feel free to reply again</strong>',
                                        ticket=tickets)
            else:
                Response.objects.create(user=request.user, text='<strong>Closed by user</strong>', ticket=tickets)
            return redirect('/tickets/id/' + str(ticket_id))
        else:
            return redirect('/tickets')
    else:
        return


def ticket_unblock(request, ticket_id):
    if not request.user.is_authenticated:
        return redirect('/')
    tickets = Ticket.objects.filter(id=ticket_id)
    if tickets.count() != 0:
        if request.user.is_staff:
            tickets = Ticket.objects.filter(id=ticket_id).first()
            tickets.blocked = False
            tickets.save()
            return redirect('/tickets/id/' + str(ticket_id))
        else:
            return redirect('/tickets')
    else:
        return render(request, 'Main/templates/404.html', status=404)


def ticket_block(request, ticket_id):
    if not request.user.is_authenticated:
        return redirect('/')
    tickets = Ticket.objects.filter(id=ticket_id)
    if tickets.count() != 0:
        if request.user.is_staff:
            tickets = Ticket.objects.filter(id=ticket_id).first()
            tickets.blocked = True
            tickets.save()
            if request.user.is_staff:
                Response.objects.create(user=request.user, text='<strong>Administrator blocked possibility to '
                                                                'answer for this ticket. Keep on mind opening more '
                                                                'ticket could affect ban</strong>',
                                        ticket=tickets)
            return redirect('/tickets/id/' + str(ticket_id))
        else:
            return redirect('/tickets')
    else:
        return render(request, 'Main/templates/404.html', status=404)


def ticket_delete(request, ticket_id):
    if not request.user.is_authenticated:
        return redirect('/')
    tickets = Ticket.objects.filter(id=ticket_id)
    if tickets.count() != 0:
        if request.user.is_staff:
            tickets = Ticket.objects.filter(id=ticket_id).first()
            tickets.delete()
            return redirect('/tickets')
        else:
            return redirect('/tickets')
    else:
        return render(request, 'Main/templates/404.html', status=404)


def ticket_view(request, ticket_id):
    if not request.user.is_authenticated:
        return redirect('/')
    tickets = Ticket.objects.filter(id=ticket_id)
    if tickets.count() != 0:
        if tickets.first().user == request.user or request.user.is_staff:
            reply = Response.objects.filter(ticket=tickets.first())
            context = {
                'replies': reply,
                'ticket': tickets.first(),
                'user': request.user,
                'SERVER_NAME': SERVER_NAME,
                'Title': 'Ticket',
            }
            if tickets.first().blocked is True:
                context = {
                    'replies': reply,
                    'ticket': tickets.first(),
                    'user': request.user,
                    'SERVER_NAME': SERVER_NAME,
                    'Title': 'Ticket',
                    'Blocked': True,
                }
                return render(request, 'Tickets/ticket.html', context)
            if request.method == 'POST':
                forms = ValidateResponse(request.POST)
                if forms.is_valid():
                    Response.objects.create(user=request.user, ticket=tickets.first(), text=request.POST['text'])
                    tickets = Ticket.objects.filter(id=ticket_id).first()
                    if not request.user.is_staff:
                        tickets.solved = False
                        tickets.save()
                    else:
                        tickets.handled_by = request.user
                        tickets.save()
                    return redirect('/tickets/id/' + str(ticket_id))
            return render(request, 'Tickets/ticket.html', context)
        else:
            return redirect('/tickets')
    else:
        return render(request, 'Main/templates/404.html', status=404)
