from django.test import TestCase
from django.urls import reverse
from .models import Blog


class BlogDetailTest(TestCase):

    def setUp(self):
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test content'
        )
        self.url = reverse(
            'blog_detail',
            kwargs={'pk': self.blog.pk}
        )

    def test_detail_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_blog_in_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['blog'].pk, self.blog.pk)

    def test_initial_likes_are_zero(self):
        self.assertEqual(self.blog.likes, 0)

    def test_likes_increase_after_visit(self):
        self.client.get(self.url)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.likes, 1)

    def test_likes_increase_after_second_visit(self):
        self.client.get(self.url)
        self.client.get(self.url)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.likes, 2)

    def test_nonexistent_blog_returns_404(self):
        url = reverse(
            'blog_detail',
            kwargs={'pk': 99999}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_blog_list_contains_title_and_link(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.blog.title)
        self.assertContains(response, self.url)