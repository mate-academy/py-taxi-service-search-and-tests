from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

HOME_URL = reverse("taxi:index")
MANUFACTURERS_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
URLS = [
    HOME_URL,
    MANUFACTURERS_LIST_URL,
    CAR_LIST_URL,
    DRIVER_LIST_URL,
    reverse("taxi:car-create"),
    reverse("taxi:car-delete", kwargs={"pk": 1}),
    reverse("taxi:car-detail", kwargs={"pk": 1}),
    reverse("taxi:car-update", kwargs={"pk": 1}),
    reverse("taxi:driver-create"),
    reverse("taxi:driver-delete", kwargs={"pk": 1}),
    reverse("taxi:driver-detail", kwargs={"pk": 1}),
    reverse("taxi:driver-update", kwargs={"pk": 1}),
    reverse("taxi:manufacturer-create"),
    reverse("taxi:manufacturer-delete", kwargs={"pk": 1}),
    reverse("taxi:manufacturer-update", kwargs={"pk": 1}),
]


class PublicTest(TestCase):

    def test_login_required_to_all_pages(self) -> None:
        for url in URLS:
            with self.subTest(url):
                response = self.client.get(url)

                self.assertNotEqual(response.status_code, 200)


class PrivateTest(TestCase):

    def test_access_with_login(self) -> None:
        user = get_user_model().objects.create(
            username="test",
            password="test_password",
        )
        self.client.force_login(user)
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        Car.objects.create(model="test", manufacturer=manufacturer)
        for url in URLS:
            with self.subTest(url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)


class HomePrivateTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_info_on_page(self) -> None:
        manufacturer = None
        for manufacturers_count in range(1, 5):
            manufacturer = Manufacturer.objects.create(
                name=f"test_{manufacturers_count}",
                country="test_county"
            )
            response = self.client.get(HOME_URL)
            self.assertEqual(
                response.context["num_manufacturers"],
                manufacturers_count
            )

        for cars_count in range(1, 4):
            Car.objects.create(model="test", manufacturer=manufacturer)
            response = self.client.get(HOME_URL)
            self.assertEqual(
                response.context["num_cars"],
                cars_count
            )
        response = self.client.get(HOME_URL)
        self.assertEqual(response.context["num_drivers"], 1)
