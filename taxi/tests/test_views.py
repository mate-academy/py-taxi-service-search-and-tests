from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_DETAIL_URL = reverse("taxi:driver-detail",
                             kwargs={"pk": 1})
CARS_DETAIL_URL = reverse("taxi:car-detail",
                          kwargs={"pk": 1})


class PublicViewTests(TestCase):
    def test_list_login_required_list(self):
        tests = [DRIVERS_URL, CARS_URL, MANUFACTURERS_URL]
        for test in tests:
            res = self.client.get(test)
            self.assertNotEqual(res.status_code, 200)

    def test_detail_login_required_list(self):
        tests = [
            DRIVERS_DETAIL_URL,
            CARS_DETAIL_URL
        ]
        for test in tests:
            res = self.client.get(test)
            self.assertNotEqual(res.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password"
        )
        self.client.force_login(self.user)

    def test_logged_in_page_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford"
        )
        Car.objects.create(
            model="Mustang",
            manufacturer=manufacturer
        )
        tests = [
            self.client.get(MANUFACTURERS_URL),
            self.client.get(CARS_URL)
        ]

        for test in tests:
            self.assertEqual(test.status_code, 200)


class PrivateManufacturerListTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            "test",
            "password",
        )
        for i in range(5):
            Manufacturer.objects.create(
                name=f"Manufacturer{i}", country=f"Country{i}"
            )

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.response = self.client.get(MANUFACTURERS_URL)

    def test_retrieve_manufacturers(self):
        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(
            list(self.response.context["manufacturer_list"]),
            list(manufacturer_list),
        )
        self.assertTemplateUsed(self.response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_search(self):
        response = self.client.get(MANUFACTURERS_URL + "?name=artur")
        queryset_searched = Manufacturer.objects.filter(
            name__icontains="artur",
        )
        self.assertQuerysetEqual(
            response.context["manufacturer_list"], queryset_searched
        )
