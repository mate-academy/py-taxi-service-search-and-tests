from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


INDEX = reverse("taxi:index")


class PublicIndexTest(TestCase):

    def test_index_login_required(self):
        response = self.client.get(INDEX)

        self.assertNotEquals(response.status_code, 200)


class PrivateIndexTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123456"
        )

        self.client.force_login(self.user)

        for _ in range(3):
            manufacturer = Manufacturer.objects.create(
                name=f"Test {_}",
                country="Test Kingdom"
            )
            if _ == 2:
                Car.objects.create(
                    model=f"Test model {_}",
                    manufacturer=manufacturer
                )

            for i in range(2):
                get_user_model().objects.create_user(
                    username=f"test{_}{i}",
                    password="test123456",
                    license_number=f"LIC123{_}{i}"
                )

    def test_retrieve_index(self):

        response = self.client.get(INDEX)

        for _ in range(5):
            response = self.client.get(INDEX)

        manufacturers = Manufacturer.objects.count()
        cars = Car.objects.count()
        drivers = get_user_model().objects.count()
        num_visits = 6

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.context["num_drivers"],
            drivers
        )
        self.assertEquals(
            response.context["num_cars"],
            cars
        )
        self.assertEquals(
            response.context["num_manufacturers"],
            manufacturers
        )
        self.assertEquals(
            response.context["num_visits"],
            num_visits
        )
