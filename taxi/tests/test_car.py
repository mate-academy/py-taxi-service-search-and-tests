from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Car, Manufacturer


CAR_ID = 1
CARS_LIST_URL = reverse("taxi:car-list")
CARS_DETAIL_URL = reverse("taxi:car-detail", args=[CAR_ID])


class PublicCarTests(TestCase):
    def test_login_required_list_page(self):
        resp = self.client.get(CARS_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_detail_page(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        Car.objects.create(
            id=CAR_ID,
            model="Test model",
            manufacturer=manufacturer,
        )

        resp = self.client.get(CARS_DETAIL_URL)

        self.assertNotEqual(resp.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="testpassword12345",
            license_number="ADR12345",
        )

        self.client.force_login(self.user)

    def test_retrieve_list_page_with_search_field(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        Car.objects.create(
            model="Test model 1",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Test model 2",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Test model 3",
            manufacturer=manufacturer,
        )

        resp = self.client.get(CARS_LIST_URL)

        cars = Car.objects.all()
        form = CarSearchForm()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["car_list"]),
            list(cars),
        )
        self.assertEqual(
            resp.context["car_search_form"].is_valid(),
            form.is_valid()
        )

    def test_retrieve_detail_page(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        Car.objects.create(
            id=CAR_ID,
            model="Test model 1",
            manufacturer=manufacturer,
        )

        resp = self.client.get(CARS_DETAIL_URL)

        car = Car.objects.get(id=CAR_ID)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.context["car"],
            car,
        )
