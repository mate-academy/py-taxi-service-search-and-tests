from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class CarDetailLoginTest(TestCase):
    def test_login_required(self) -> None:
        respons = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(respons.status_code, 200)
        self.assertRedirects(respons, r"/accounts/login/?next=%2Fcars%2F")


class ManufacturerSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "psswd2022"
        )
        self.client.force_login(self.user)

    def test_search_result_manufacturer(self) -> None:
        Manufacturer.objects.create(
            name="Test1Brand",
            country="TestCountry1"
        )
        Manufacturer.objects.create(
            name="Test2Brantt",
            country="TestCountry2"
        )
        Manufacturer.objects.create(
            name="TestBland",
            country="TestCountry3"
        )

        response = self.client.get(MANUFACTURER_LIST_URL + "?name=Bran")
        manufactureres = Manufacturer.objects.filter(name__icontains="Bran")

        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            manufactureres
        )
