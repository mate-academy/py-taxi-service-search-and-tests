from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="AAA12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car1.drivers.set([self.driver])
        self.car2.drivers.set([self.driver])

    def test_driver_license_listed(self):
        """
        Test that a driver's license number is in
        list_display on driver admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_listed(self):
        """
        Test that a driver's license number is on driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_add_fieldsets(self):
        """
        Test that a driver's license number are displayed
        in the add_fieldsets on the add driver admin page.
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "license_number")

    def test_cars_search_field(self):
        """
        Test that the search field works correctly on the car admin page.
        """
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url, {"q": "Corolla"})
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)

    def test_cars_list_filter(self):
        """
        Test that the list filter works correctly on the car admin page.
        """
        url = reverse("admin:taxi_car_changelist")
        response = (
            self.client.get(
                url,
                {"manufacturer__id__exact": self.manufacturer.id}
            )
        )
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
