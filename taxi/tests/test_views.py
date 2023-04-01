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


class DriverCreateDeleteTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="dirvertest",
            first_name="First",
            last_name="Lasts",
            license_number="CAD25252",
            password="drivepass22",
        )

        self.client.force_login(self.user)

    def test_driver_created(self) -> None:
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            get_user_model().objects.filter(id=self.user.id).exists()
        )

    def test_driver_deleted(self) -> None:
        new_driver = get_user_model().objects.create(
            username="random.test",
            license_number="TTT11112",
            first_name="Temp",
            last_name="Temps",
            password="222asdfg",
        )

        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": new_driver.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=new_driver.id).exists()
        )
