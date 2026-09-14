from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Driver, Manufacturer


class PrivateViewAccessTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="ComplexP@ssw0rd123",
            license_number="AAA12345",
        )

    def test_unauthenticated_access_redirects(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_access_success(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")


class SearchViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="searchuser",
            password="ComplexP@ssw0rd123",
            license_number="BBB12345",
        )
        self.client.force_login(self.user)

        # Cars & Manufacturers setup
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Toyota Corolla", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Toyota Camry", manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="Ford Focus", manufacturer=self.manufacturer
        )

        # Drivers setup
        self.driver1 = Driver.objects.create_user(
            username="john_doe",
            password="ComplexP@ssw0rd123",
            license_number="AAA11111",
        )
        self.driver2 = Driver.objects.create_user(
            username="john_smith",
            password="ComplexP@ssw0rd123",
            license_number="AAA22222",
        )
        self.driver3 = Driver.objects.create_user(
            username="alice_wong",
            password="ComplexP@ssw0rd123",
            license_number="AAA33333",
        )

        # Manufacturers search setup
        self.man1 = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        self.man2 = Manufacturer.objects.create(
            name="Hyundai",
            country="South Korea"
        )
        self.man3 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_car_search_filter(self):
        url = reverse("taxi:car-list") + "?model=toyota"
        response = self.client.get(url)
        self.assertIn(self.car1, response.context["car_list"])
        self.assertIn(self.car2, response.context["car_list"])
        self.assertNotIn(self.car3, response.context["car_list"])

    def test_driver_search_filter(self):
        url = reverse("taxi:driver-list") + "?username=john"
        response = self.client.get(url)
        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertIn(self.driver2, response.context["driver_list"])
        self.assertNotIn(self.driver3, response.context["driver_list"])

    def test_manufacturer_search_filter(self):
        url = reverse("taxi:manufacturer-list") + "?name=H"
        response = self.client.get(url)
        self.assertIn(self.man1, response.context["manufacturer_list"])
        self.assertIn(self.man2, response.context["manufacturer_list"])
        self.assertNotIn(self.man3, response.context["manufacturer_list"])
