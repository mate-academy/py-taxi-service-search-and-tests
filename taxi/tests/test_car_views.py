from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Car, Manufacturer, Driver

CAR_LIST = reverse("taxi:car-list")


class PublicCarViewListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            first_name="Test",
            last_name="User",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        driver1 = Driver.objects.create(
            username="driver1",
            license_number="ABC12345",
            password="password1",
        )
        driver2 = Driver.objects.create(
            username="driver2",
            license_number="DEF67890",
            password="password2",
        )

        car1 = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer,
        )
        car1.drivers.set([driver1])

        car2 = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer,
        )
        car2.drivers.set([driver2])

        car3 = Car.objects.create(
            model="Prius",
            manufacturer=manufacturer,
        )
        car3.drivers.set([driver1, driver2])

    def test_retrieve_car(self):
        response = self.client.get(CAR_LIST)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_view_search(self):
        """
        Search for cars with the name 'Camry'
        Verify that the search form is present in the context
        Verify that the filtered manufacturers are present in the context
        """
        form_data = {
            "model": "Camry",
        }
        response = self.client.get(reverse("taxi:car-list"), data=form_data)
        self.assertEqual(response.status_code, 200)

        form = response.context["search_form"]
        self.assertIsInstance(form, CarSearchForm)

        car_list = response.context["car_list"]
        self.assertEqual(len(car_list), 1)
        self.assertEqual(car_list[0].model, "Camry")
