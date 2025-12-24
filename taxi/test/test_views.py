from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Driver, Manufacturer


class LoginTestCase(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(res.status_code, 200)


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.login(
            username="testuser",
            password="testpass"
        )

    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="Subaru",
            country="Japan"
        )
        Driver.objects.create(
            username="reichikku",
            first_name="Slawa",
            last_name="Melnyk",
            license_number="IKO0448"
        )
        Car.objects.create(
            model="Subaru Forester",
            manufacturer=Manufacturer.objects.get(name="Subaru"),
        )


class IndexViewTest(BaseTestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_context_data(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(
            response.context["num_drivers"],
            Driver.objects.count()
        )
        self.assertEqual(
            response.context["num_cars"],
            Car.objects.count()
        )
        self.assertEqual(
            response.context["num_manufacturers"],
            Manufacturer.objects.count()
        )


class ManufacturerListViewTest(BaseTestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_functionality(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Subaru"}
        )
        self.assertContains(response, "Subaru")

    def setUp(self):
        super().setUp()
        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Ford")
        Manufacturer.objects.create(name="Tesla")

    def test_search_returns_correct_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Ford"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ford")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")

    def test_search_returns_all_if_no_query(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")
        self.assertContains(response, "Tesla")


class DriverListViewTest(BaseTestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_functionality(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "reichikku"}
        )
        self.assertContains(response, "reichikku")


class CarListViewTest(BaseTestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_functionality(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Subaru Forester"}
        )
        self.assertContains(response, "Subaru Forester")
