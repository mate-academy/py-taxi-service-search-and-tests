from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

HOME_URL = reverse("taxi:index")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


class TestViewsLoginRequired(TestCase):
    def test_login_required_home(self):
        response = self.client.get(HOME_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_cars_list(self):
        response = self.client.get(CARS_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_drivers_list(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_manufacturers_list(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEquals(response.status_code, 200)


class TestViewsPagesForRegisteredUser(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="rambo1982",
            password="JustWantToEatButHaveToKill82",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Volvo", country="Sweden")

        response = self.client.get(MANUFACTURERS_URL)
        self.assertEquals(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
