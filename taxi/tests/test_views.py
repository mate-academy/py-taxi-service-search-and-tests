from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Alfa Romeo", country="Italy")
        Manufacturer.objects.create(name="BMW", country="Germany")

    def test_get_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=B"
        )
        self.assertEqual(response.status_code, 200)
        actual = response.context.get("manufacturer_list")
        expected = Manufacturer.objects.filter(name__icontains="B")
        self.assertEqual(list(actual), list(expected))
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=BMW"
        )
        actual = response.context.get("manufacturer_list")
        expected = Manufacturer.objects.filter(name__icontains="BMW")
        self.assertEqual(list(actual), list(expected))

    def test_empty_field_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name="
        )
        self.assertEqual(response.status_code, 200)
        actual = response.context.get("manufacturer_list")
        expected = Manufacturer.objects.all()
        self.assertEqual(list(actual), list(expected))


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        alfa = Manufacturer.objects.create(name="Alfa Romeo", country="Italy")
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(model="Alfa Romeo Giulia", manufacturer=alfa)
        Car.objects.create(model="BMW M8", manufacturer=bmw)

    def test_get_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=BMW")
        self.assertEqual(response.status_code, 200)
        actual = response.context.get("car_list")
        expected = Car.objects.filter(model__icontains="BMW")
        self.assertEqual(list(actual), list(expected))
        response = self.client.get(reverse("taxi:car-list") + "?model=Giulia")
        actual = response.context.get("car_list")
        expected = Car.objects.filter(model__icontains="Giulia")
        self.assertEqual(list(actual), list(expected))

    def test_empty_field_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=")
        self.assertEqual(response.status_code, 200)
        actual = response.context.get("car_list")
        expected = Car.objects.all()
        self.assertEqual(list(actual), list(expected))


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="AMD12345",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="user",
            password="user123",
            license_number="AYT54321"
        )
        get_user_model().objects.create_user(
            username="jason_statham",
            password="coolguy123",
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
