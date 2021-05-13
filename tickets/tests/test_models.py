from django.test import TestCase
from ..models import Response, Ticket, User


class TestModels(TestCase):
    def test_models(self):
        # Test Ticket model
        admin = User.objects.create_user(username='admin', email='test@case.com', nickname='Test', password='test')
        Ticket.objects.create(title='Test', user=admin, problem='TestCase')
        obj = Ticket.objects.filter(user=admin).first()
        obj2 = Ticket.objects.filter(title='Test').first()
        self.assertEqual(obj.id, obj2.id)
        # Test response model
        Response.objects.create(ticket=obj, user=admin, text='Test')
        self.assertIsNotNone(Response.objects.filter(text='Test', user=admin))
