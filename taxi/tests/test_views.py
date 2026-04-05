from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = "Testclient",
            email = "test_email@gmail.com",
            password = "12341234!",
            first_name = "Testfirst",
            last_name = "Testlast",
            license_number = "ABC12345",
        )
        self.client.force_login(self.user)
        self.manufacturer_one = Manufacturer.objects.create(
            name = "Toyota",
            country = "Japan",
        )

        self.manufacturer_two = Manufacturer.objects.create(
            name = "BMW",
            country = "Germany",
        )

    def test_search_manufacturer_by_name(self):
        url = reverse('taxi:manufacturer-list') + "?manufacturer=toyota"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")






class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = "Testclient",
            email = "test_email@gmail.com",
            password = "12341234!",
            first_name = "Testfirst",
            last_name = "Testlast",
            license_number = "ABC12345",
        )
        self.client.force_login(self.user)
        self.car_one = Car.objects.create(
            model = "Corsa",
            manufacturer = Manufacturer.objects.create(
                name = "Opel",
                country = "Japan",
            ),
        )
        self.car_one.drivers.add(self.user)

        self.car_two = Car.objects.create(
            model = "Prius",
            manufacturer = Manufacturer.objects.create(
                name = "Toyota",
                country = "Japan",
            ),
        )
        self.car_two.drivers.add(self.user)

    def test_search_car_by_name(self):
        url = reverse('taxi:car-list') + "?car=corsa"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "corsa")
        self.assertNotContains(response, "prius")



class DriverSearchTests(TestCase):
    def setUp(self):
        self.driver_one = get_user_model().objects.create_user(
            username = "Testclient",
            email = "test_email@gmail.com",
            password = "12341234!",
            first_name = "Testfirst",
            last_name = "Testlast",
            license_number = "ABC12345",
        )
        self.client.force_login(self.driver_one)
        self.driver_two = get_user_model().objects.create_user(
            username="siema",
            email="test_email1@gmail.com",
            password="123412341!",
            first_name="Testfirst1",
            last_name="Testlast1",
            license_number="ABC12341",
        )


    def test_search_driver_by_name(self):
        url = reverse('taxi:driver-list') + "?driver=Testclient"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testclient")
        self.assertNotContains(response, "siema")


class Public(TestCase):
    def test_login_required_for_all_private_views(self):
        urls = [
            reverse('taxi:manufacturer-list'),
            reverse('taxi:car-list'),
            reverse('taxi:driver-list'),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)




class PrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Testclient",
            email="test_email@gmail.com",
            password="12341234!",
            first_name="Testfirst",
            last_name="Testlast",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)
        self.test_manufacturer = Manufacturer.objects.create(
            name = "Toyota",
            country = "Japan",
        )
        self.test_car = Car.objects.create(
            model = "Corsa",
            manufacturer = self.test_manufacturer,
        )
        self.test_car.drivers.add(self.user)


    def test_car_detail_view_displays_driver(self):
        url = reverse('taxi:car-detail', args=[self.test_car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
