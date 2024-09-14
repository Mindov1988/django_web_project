from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from electronics_shop.electronics.models import Order


class DashboardViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.orders = [
            Order.objects.create(user=self.user, total_price=100.00, cart_data={'item1': 1}),
            Order.objects.create(user=self.user, total_price=50.00, cart_data={'item2': 2}),
        ]
        self.url = reverse('dashboard')

    def test_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')

        self.assertIn('orders', response.context)
        context_order_ids = [order.id for order in response.context['orders']]
        expected_order_ids = [order.id for order in self.orders]
        self.assertCountEqual(context_order_ids, expected_order_ids)

    def test_dashboard_view_unauthenticated(self):
        self.client.logout()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')

        self.assertIn('orders', response.context)
        self.assertEqual(response.context['orders'], None)

