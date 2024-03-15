from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test1", country="USA")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="test1", country="USA")
        Car.objects.create(manufacturer=manufacturer, model="test")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)


class CarListViewSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")
        toyota_manufacturer = Manufacturer.objects.create(name="Toyota")
        honda_manufacturer = Manufacturer.objects.create(name="Honda")
        bmw_manufacturer = Manufacturer.objects.create(name="BMW")

        Car.objects.create(
            model="Toyota Camry",
            manufacturer=toyota_manufacturer
        )
        Car.objects.create(
            model="Honda Accord",
            manufacturer=honda_manufacturer
        )
        Car.objects.create(model="BMW 4 Series", manufacturer=bmw_manufacturer)

    def test_car_list_view_with_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota Camry")
        self.assertNotContains(response, "Honda Accord")
        self.assertNotContains(response, "BMW 4 Series")


class PublicIndexTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(res.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)


class ToogleAssignToCarTest(TestCase):
    def setUp(self) -> None:
        get_user_model().objects.create_user(
            username="test username",
            password="test_password",
            license_number="FGH1331"
        )

        get_user_model().objects.create_user(
            username="test_second username",
            password="test_password_second",
            license_number="FGH1333"
        )

        Manufacturer.objects.create(
            name="test manufacturer1",
            country="test country1"
        )

        Manufacturer.objects.create(
            name="test manufacturer2",
            country="test country2"
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
            username="test_user",
            password="test_password",
            license_number="GHF33222"
        )

        self.client.force_login(self.user)

    def test_toggle_assign_to_car_add_driver(self) -> None:
        driver = self.user
        car = Car.objects.get(pk=1)

        self.client.get(reverse("taxi:toggle-car-assign", args=[car.id]))
        response = self.client.get(reverse("taxi:car-detail", args=[car.id]))

        self.assertIn(driver, response.context["car"].drivers.all())
