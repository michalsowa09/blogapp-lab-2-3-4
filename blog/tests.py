from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post
from django.urls import reverse

class BlogAndApiTests(TestCase):
    def setUp(self):
        # Tworze dane testowe
        self.user = User.objects.create_user(username='tester', password='password123')
        self.post = Post.objects.create(
            title='Testowy Post Lab5',
            content='Treść testowa',
            author=self.user,
            status='published'
        )

    def test_post_content(self):
        """Test 1: Sprawdza czy model posta działa poprawnie"""
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.title, 'Testowy Post Lab5')

    def test_weather_api_endpoint(self):
        """Test 2: Sprawdza czy mój własny endpoint JSON zwraca dane"""
        # Używam nazwy z urls.py aplikacji external_data
        response = self.client.get(reverse('weather_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')