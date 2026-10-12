from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver1234",
            license_number="CBN78906",
        )

    def test_driver_license_number(self):
        """
        Test that driver's license number is on admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license number is on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_page_license_number_listed(self):
        """
        Test that driver's license number is on driver add page
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="license_number"')

    def test_car_search_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        car = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer,
        )

        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url, {"q": "Camry"})

        self.assertContains(res, car.model)

    def test_car_filter_by_manufacturer(self):
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        toyota_car = Car.objects.create(
            model="Camry",
            manufacturer=toyota,
        )
        bmw_car = Car.objects.create(
            model="X5",
            manufacturer=bmw,
        )

        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(
            url,
            {"manufacturer__id__exact": toyota.id}
        )

        self.assertContains(res, toyota_car.model)
        self.assertNotContains(res, bmw_car.model)
