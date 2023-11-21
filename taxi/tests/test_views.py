from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class TestIndexView(TestCase):
    def test_index_login_required(self) -> None:
        url = reverse("taxi:index")
        res = self.client.get(url)
        self.assertNotEquals(res, 200)


class TestPublicManufacturerListView(TestCase):
    def test_manufacturer_list_view_login_required(self) -> None:
        self.url = reverse("taxi:manufacturer-list")
        res = self.client.get(self.url)
        self.assertNotEquals(res.status_code, 200)


class TestPrivateManufacturerListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUserName",
            password="test-password"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:manufacturer-list")

    def test_retrieve_manufacturers(self) -> None:
        Manufacturer.objects.create(
            name="TestName1",
            country="TestCountry1"
        )

        Manufacturer.objects.create(
            name="TestName2",
            country="TestCountry2"
        )

        res = self.client.get(self.url)

        self.assertEquals(res.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEquals(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_manufacturers_list_used_template(self):
        self.assertTemplateUsed("taxi:manufacturer-list")


class TestPublicDriverListView(TestCase):
    def test_driver_list_view_login_required(self) -> None:
        self.url = reverse("taxi:driver-list")
        res = self.client.get(self.url)
        self.assertNotEquals(res.status_code, 200)


class TestPrivateDriverListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUserName",
            password="test-password"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-list")

    def test_retrieve_manufacturers(self) -> None:
        get_user_model().objects.create_user(
            username="TestName1",
            password="test-password1",
            license_number="ABC00000"
        )

        get_user_model().objects.create_user(
            username="TestName2",
            password="test-password2",
            license_number="ABC11111"
        )

        res = self.client.get(self.url)

        self.assertEquals(res.status_code, 200)

        drivers = get_user_model().objects.all()
        self.assertEquals(
            list(res.context["object_list"]),
            list(drivers)
        )

    def test_manufacturers_list_used_template(self):
        self.assertTemplateUsed(self.url)


class TestPublicCarListView(TestCase):
    def test_manufacturer_list_view_login_required(self) -> None:
        self.url = reverse("taxi:car-list")
        res = self.client.get(self.url)
        self.assertNotEquals(res.status_code, 200)


class TestPrivateCarListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUserName",
            password="test-password"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:car-list")

    def test_retrieve_manufacturers(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestName1",
            country="TestCountry1"
        )
        Car.objects.create(
            model="TestModel1",
            manufacturer=manufacturer
        )

        Car.objects.create(
            model="TestModel2",
            manufacturer=manufacturer
        )

        res = self.client.get(self.url)

        self.assertEquals(res.status_code, 200)

        cars = Car.objects.all()
        self.assertEquals(
            list(res.context["car_list"]),
            list(cars)
        )

    def test_manufacturers_list_used_template(self):
        self.assertTemplateUsed("taxi:car-list")
