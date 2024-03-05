from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car


URL_CAR_LIST = "taxi:car-list"


class PublicCarViewTest(TestCase):
    def test_car_login_required(self) -> None:
        response = self.client.get(reverse(URL_CAR_LIST))

        self.assertRedirects(
            response,
            "/accounts/login/?next=/cars/"
        )


class PrivateCarViewTest(TestCase):
    def setUp(self) -> None:
        num_drivers = 4
        num_manufacturers = 2
        for driver_id in range(num_drivers):
            get_user_model().objects.create_user(
                username=f"test username {driver_id}",
                password=f"test12{driver_id}",
                license_number=f"AAA1234{driver_id}"
            )

        for manufacturer_id in range(num_manufacturers):
            Manufacturer.objects.create(
                name=f"test manufacturer {manufacturer_id}",
                country=f"test country {manufacturer_id}"
            )

        test_car1 = Car.objects.create(
            model="test car 1",
            manufacturer_id=1,
        )
        test_car2 = Car.objects.create(
            model="test car 2",
            manufacturer_id=2,
        )

        test_car1.drivers.set(get_user_model().objects.all()[:2])
        test_car1.drivers.set(get_user_model().objects.all()[2:])

        test_car1.save()
        test_car2.save()

        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            license_number="AAA55555"
        )

        self.client.force_login(self.user)

    def test_car_correct_template(self) -> None:
        response = self.client.get(reverse(URL_CAR_LIST))

        self.assertEqual(str(response.context["user"]), "test_username ( )")

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_list(self) -> None:
        response = self.client.get(reverse(URL_CAR_LIST))
        cars = Car.objects.all()

        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_car_list_search(self) -> None:
        response = self.client.get(reverse(URL_CAR_LIST) + "?model=1")
        car = Car.objects.filter(model="test car 1")

        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
