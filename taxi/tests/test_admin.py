from django.test import TestCase
from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Car, Manufacturer, Driver

User = get_user_model()

class AdminTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.client.login(username="admin", password="adminpass")

    def test_models_registered_in_admin(self):
        """Перевіряємо, чи зареєстровані моделі в адмінці"""
        self.assertIn(Car, site._registry)  # Перевіряємо наявність класу
        self.assertIn(Manufacturer, site._registry)
        self.assertIn(Driver, site._registry)

    def test_admin_access(self):
        """Перевіряємо, чи адміністратор може зайти в адмінку"""
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
