from django.test import TestCase
from ..models import User, Ticket
from django.test import Client


class TestView(TestCase):
    def test_tickets(self):
        # Not authed
        response = self.client.get('/tickets')
        self.assertEqual(response.status_code, 301)
        # Authed
        password = 'sjkk25nk253k'
        admin = User.objects.create_user(username='admin', email='test@case.com', nickname='Test', password=password)
        c = Client()
        c.login(username='admin', password=password)
        response = c.get('/tickets/')
        self.assertEqual(response.status_code, 200)
        # Authed ticket
        Ticket.objects.create(title='Test', user=admin, problem='TestCase')
        number = Ticket.objects.filter(user=admin).first()
        response = c.get('/tickets/id/' + str(number.id) + '/')
        self.assertEqual(response.status_code, 200)
        # Ticket that doesnt exists
        response = c.get('/tickets/id/10/')
        self.assertEqual(response.status_code, 404)
