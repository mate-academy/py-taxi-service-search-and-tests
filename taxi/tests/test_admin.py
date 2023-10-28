from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="KungFury",
            password="KilledHitlerAfter1945",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="rambo1982",
            password="JustWantToEatButHaveToKill82",
            license_number="RAM19821"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="M3",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_driver_license_number_listed(self):
        """
        Test that license number displayed on admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_listed_on_detail_page(self):
        """
        Test that license number displayed on driver detail page in admin page
        """
        url = reverse(
            "admin:taxi_driver_change", args=[self.driver.id]
        )
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
