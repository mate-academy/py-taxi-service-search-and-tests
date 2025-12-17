from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import (
    Manufacturer,
    Car,
)

User = get_user_model()


class ManufacturerModelTest(TestCase):
    def test_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota")


class CarModelTest(TestCase):
    def test_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        car = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.assertEqual(str(car), "X5")


class UserModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(
            username="sofa",
            password="test12345",
            first_name="Sofa",
            last_name="Dev",
            license_number="ABC12345",
        )
        self.assertEqual(str(user), "sofa")


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sofa",
            password="test12345",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        self.car = Car.objects.create(
            model="A4", manufacturer=self.manufacturer
        )
        self.url = reverse("taxi:car-list")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_logged_in_user_can_access(self):
        self.client.login(username="sofa", password="test12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A4")
        self.assertTemplateUsed(response, "taxi/car_list.html")


class CarDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sofa",
            password="test12345",
            license_number="ABC12345",
        )
        manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        self.car = Car.objects.create(model="A4", manufacturer=manufacturer)
        self.url = reverse("taxi:car-detail", args=[self.car.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={self.url}"
        )

    def test_logged_in_user_can_access(self):
        self.client.login(username="sofa", password="test12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A4")


class CarCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sofa",
            password="test12345",
            license_number="ABC12345",
        )
        self.url = reverse("taxi:car-create")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_logged_in_user_can_access(self):
        self.client.login(username="sofa", password="test12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sofa",
            password="test12345",
            license_number="ABC12345",
        )
        User.objects.create_user(
            username="john",
            password="test12345",
            license_number="XYZ98765",
        )
        self.client.login(username="sofa", password="test12345")

    def test_search_by_username(self):
        response = self.client.get(reverse("taxi:driver-list"), {"q": "john"})
        self.assertContains(response, "john")
        self.assertNotContains(response, "sofa")


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sofa",
            password="test12345",
            license_number="ABC12345",
        )
        self.client.login(username="sofa", password="test12345")

        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="M3", manufacturer=manufacturer)

    def test_search_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"q": "X5"})
        self.assertContains(response, "X5")
        self.assertNotContains(response, "M3")


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sofa",
            password="test12345",
            license_number="ABC12345",
        )
        self.client.login(username="sofa", password="test12345")

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Audi", country="Germany")

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"q": "Audi"}
        )
        self.assertContains(response, "Audi")
        self.assertNotContains(response, "Toyota")
