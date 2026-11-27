from django.test import Client, TestCase

from .models import Driver


class TestDriverSearch(TestCase):
    def test_driver_search(self):
        Driver.objects.create(username="ana")
        user = Driver.objects.create_user(username="ana")
        self.client.force_login(user)
        response = self.client.get("/drivers/", {"username": "ana"})
        self.assertContains(response, "ana")
        self.assertNotContains(response, "bruno")
