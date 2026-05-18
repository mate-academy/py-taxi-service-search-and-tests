from django.test import TestCase
from django.urls import reverse


class LoginRequiredTests(TestCase):
    def test_driver_list_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('taxi:driver-list')}",
        )

    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('taxi:car-list')}",
        )

    def test_manufacturer_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            (
                f"{reverse('login')}?next="
                f"{reverse('taxi:manufacturer-list')}"
            ),
        )
