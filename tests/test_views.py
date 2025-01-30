from http.client import responses

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicCarListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)


class PublicDriverListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class PublicManufacturerListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Ferrari", country="Italy")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_get_manufacturer_list(self):

        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=F"
        )
        self.assertEqual(response.status_code, 200)

        actual = response.context.get("manufacturer_list")
        expected = Manufacturer.objects.filter(name__icontains="F")

        self.assertEqual(list(actual), list(expected))

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Ford"
        )
        actual = response.context.get("manufacturer_list")
        expected = Manufacturer.objects.filter(name__icontains="Ford")

        self.assertEqual(list(actual), list(expected))

    def test_empty_field_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name="
        )

        self.assertEqual(response.status_code, 200)

        actual = response.context.get("manufacturer_list")
        expected = Manufacturer.objects.all()

        self.assertEqual(list(actual), list(expected))


class PrivateCarListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

        ferrari = Manufacturer.objects.create(name="Ferrari", country="Italy")
        ford = Manufacturer.objects.create(name="Ford", country="USA")

        Car.objects.create(model="Ferrari FS90 Spider", manufacturer=ferrari)
        Car.objects.create(model="Ferrari Roma", manufacturer=ferrari)
        Car.objects.create(model="Ford Fusion", manufacturer=ford)
        Car.objects.create(model="Ford Escape Sport", manufacturer=ford)

    def test_get_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Ford")

        self.assertEqual(response.status_code, 200)

        actual = response.context.get("car_list")
        expected = Car.objects.filter(model__icontains="Ford")

        self.assertEqual(list(actual), list(expected))

        response = self.client.get(reverse("taxi:car-list") + "?model=FS90")
        actual = response.context.get("car_list")
        expected = Car.objects.filter(model__icontains="FS90")

        self.assertEqual(list(actual), list(expected))

    def test_empty_field_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=")

        self.assertEqual(response.status_code, 200)

        actual = response.context.get("car_list")
        expected = Car.objects.all()

        self.assertEqual(list(actual), list(expected))


class PrivateDriverListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="AMD12345",
        )
        self.client.force_login(self.user)

        get_user_model().objects.create_user(
            username="user",
            password="user1234",
            license_number="AYT54321"
        )
        get_user_model().objects.create_user(
            username="jason_statham",
            password="coolguy1234",
            license_number="JSN00000"
        )

    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=Jason"
        )

        self.assertEqual(response.status_code, 200)

        actual = response.context.get("driver_list")
        expected = get_user_model().objects.filter(username__icontains="Jason")

        self.assertEqual(list(actual), list(expected))

    def test_empty_field_search(self):
        response = self.client.get(reverse("taxi:driver-list") + "?username=")
        self.assertEqual(response.status_code, 200)

        actual = response.context.get("driver_list")
        expected = get_user_model().objects.all()

        self.assertEqual(list(actual), list(expected))
