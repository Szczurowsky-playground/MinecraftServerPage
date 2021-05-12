from django.test import TestCase
from ..models import Post, User


class PostTest(TestCase):
    def test_post(self):
        password = 'sjkk25nk253k'
        admin = User.objects.create(username='admin', email='test@case.com', nickname='Test')
        admin.set_password(password)
        admin.save()
        Post.objects.create(author= admin,title='TestCase', image='TestCaseIMG', text='RandomText')
        obj = Post.objects.filter(title='TestCase').first()
        self.assertEqual(obj.image, 'TestCaseIMG')
