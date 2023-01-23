from django.test import TestCase


class LoginTestCase(TestCase):

    def test_login(self):
        response = self.client.get("/manufacturers/")
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")
