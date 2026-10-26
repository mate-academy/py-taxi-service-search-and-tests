from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", args=[1])
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", args=[1])


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 302)

    def test_create_manufacturer(self):
        res = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(res.status_code, 302)

    def test_update_manufacturer(self):
        res = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertEqual(res.status_code, 302)

    def test_delete_manufacturer(self):
        res = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertEqual(res.status_code, 302)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test")
        Manufacturer.objects.create(name="test2")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer_post(self):
        response = self.client.post(MANUFACTURER_CREATE_URL, {
            "name": "test",
            "country": "US",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="test").exists())

    def test_update_manufacturer_post(self):
        manufacturer = Manufacturer.objects.create(
            name="old name",
            country="old country",
        )
        url = reverse("taxi:manufacturer-update", args=[manufacturer.pk])
        response = self.client.post(url, {
            "name": "new name",
            "country": "new country",
        })
        self.assertEqual(response.status_code, 302)
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, "new name")
        self.assertEqual(manufacturer.country, "new country")

    def test_delete_manufacturer_post(self):
        manufacturer = Manufacturer.objects.create(
            name="old name",
            country="old country",
        )
        url = reverse("taxi:manufacturer-delete", args=[manufacturer.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        manufacturer_exists = (
            Manufacturer.objects.filter(pk=manufacturer.pk).exists()
        )
        self.assertFalse(manufacturer_exists)


class DriverSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_test",
            password="test123",
            license_number="test_license_number",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="user_test2",
            password="test123",
            license_number="test_license_number2",
        )
        get_user_model().objects.create_user(
            username="user_test3",
            password="test123",
            license_number="test_license_number3",
        )

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=user_test2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user_test2")
        self.assertNotContains(response, "user_test3")


class CarSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_test",
            password="test123",
            license_number="test_license_number",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="US",
        )
        Car.objects.create(
            model="test1",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="test2",
            manufacturer=self.manufacturer,
        )

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=test1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test1")
        self.assertNotContains(response, "test2")


class ManufacturerSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_test",
            password="test123",
            license_number="test_license_number",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="test1",
            country="US",
        )
        Manufacturer.objects.create(
            name="test2",
            country="US",
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=test1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test1")
        self.assertNotContains(response, "test2")
