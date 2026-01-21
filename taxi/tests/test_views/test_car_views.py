from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from taxi.models import Car, Manufacturer, Driver

CAR_LIST_VIEW_URL = reverse_lazy("taxi:car-list")


class PublicCarListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_VIEW_URL)

        self.assertEqual(response.status_code, 302)


class PrivateCarListView(TestCase):
    def setUp(self):
        self.driver_user = get_user_model().objects.create_user(
            username="user_driver",
            password="driver_password",
        )

        self.client.force_login(self.driver_user)

        self.created_manufacturer = Manufacturer.objects.create(
            name="M-1",
            country="C-1",
        )

        self.cars = Car.objects.bulk_create([
            Car(model="M-1", manufacturer=self.created_manufacturer),
            Car(model="M-2", manufacturer=self.created_manufacturer),
        ])

        self.response = self.client.get(CAR_LIST_VIEW_URL)

    def test_list_view_should_display_data(self):
        self.assertEqual(
            list(self.response.context["car_list"]),
            list(self.cars)
        )

    def test_car_search_field(self):
        data = {
            "model": "M-1",
        }

        self.response = self.client.get(CAR_LIST_VIEW_URL, data=data)

        self.cars = Car.objects.filter(model__icontains=data["model"])

        self.assertEqual(
            list(self.response.context["car_list"]),
            list(self.cars)
        )


class PrivateCarDetailViewTest(TestCase):
    def setUp(self):
        self.driver_user = get_user_model().objects.create_user(
            username="user_driver",
            password="driver_password",
        )

        self.client.force_login(self.driver_user)

        self.created_manufacturer = Manufacturer.objects.create(
            name="M-1",
            country="C-1",
        )

        self.created_drivers = Driver.objects.bulk_create(
            [
                Driver(
                    username="D-1",
                    password="d-1-password",
                    license_number="JIM26531"
                ),
                Driver(
                    username="D-2",
                    password="d-2-password",
                    license_number="DOM26531"
                ),
            ],
        )

        self.created_car = Car.objects.create(
            model="M-1",
            manufacturer=self.created_manufacturer
        )

        self.created_car.drivers.set(self.created_drivers)

        self.url = reverse_lazy(
            "taxi:car-detail",
            kwargs={"pk": self.created_car.pk}
        )

        self.response = self.client.get(self.url)

    def test_login_required(self):
        self.assertTrue(self.response.status_code, 200)

    def test_should_display_detail_data(self):
        self.assertEqual(self.response.context["car"], self.created_car)
