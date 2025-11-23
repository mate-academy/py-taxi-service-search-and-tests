from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerViewTest(TestCase):
    def test_logen_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverViewTest(TestCase):
    def test_logen_required(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)


class PublicCarViewTest(TestCase):
    def test_logen_required(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user123",
            license_number="123VVFАD",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(
            name="Manufacturer",
            country="US",
        )
        Manufacturer.objects.create(
            name="Manufacturer2",
            country="kiev",
        )
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)


User = get_user_model()


class CarListViewQuerysetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )
        self.m1 = Manufacturer.objects.create(name="Toyota")
        self.m2 = Manufacturer.objects.create(name="BMW")

        Car.objects.create(model="Corolla", manufacturer=self.m1)
        Car.objects.create(model="Camry", manufacturer=self.m1)
        Car.objects.create(model="X5", manufacturer=self.m2)
        Car.objects.create(model="X3", manufacturer=self.m2)
        self.client.force_login(self.user)

    def test_queryset_filtering(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Corolla")
        self.assertEqual(response.status_code, 200)
        cars = response.context["object_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Corolla")

    def test_queryset_no_filter(self):
        response = self.client.get(reverse("taxi:car-list"))
        cars = response.context["object_list"]
        self.assertEqual(len(cars), 4)


class DriverListViewQuerysetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="21313sa",
            license_number="12345"
        )

        Driver.objects.create(
            username="testuser1",
            password="21313swa",
            license_number="123444"
        )
        Driver.objects.create(
            username="testuser2",
            password="21313saa",
            license_number="12345e"
        )
        Driver.objects.create(
            username="testuser3",
            password="21313sda",
            license_number="123452"
        )
        self.client.force_login(self.user)

    def test_queryset_filtering(self):
        res = self.client.get(
            reverse("taxi:driver-list") + "?username=testuser1"
        )
        self.assertEqual(res.status_code, 200)
        drivers = res.context["object_list"]
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "testuser1")

    def test_queryset_no_filter(self):
        res = self.client.get(reverse("taxi:driver-list"))
        drivers = res.context["object_list"]
        self.assertEqual(len(drivers), 4)


class ManufacturerListViewQuerysetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="21313sa",
            license_number="12345"
        )

        Manufacturer.objects.create(name="Toyota", country="US")
        Manufacturer.objects.create(name="BMW", country="Lutsk")
        Manufacturer.objects.create(name="Lexus", country="Japan")
        self.client.force_login(self.user)

    def test_queryset_filtering(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Toyota"
        )
        self.assertEqual(res.status_code, 200)
        manufacturers = res.context["object_list"]
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "Toyota")

    def test_queryset_no_filter(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = res.context["object_list"]
        self.assertEqual(len(manufacturers), 3)
