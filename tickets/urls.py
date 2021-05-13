from django.urls import path
from .views import home, ticket_view, ticket_close, ticket_delete, ticket_block, ticket_unblock

app_name = 'tickets'

urlpatterns = [
    path('', home, name='Tickets'),
    path('id/<int:ticket_id>/', ticket_view, name='Tickets'),
    path('id/<int:ticket_id>/close/', ticket_close, name='Ticket'),
    path('id/<int:ticket_id>/delete/', ticket_delete, name='Ticket'),
    path('id/<int:ticket_id>/block/', ticket_block, name='Ticket'),
    path('id/<int:ticket_id>/unblock/', ticket_unblock, name='Ticket'),
]
