from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class PublicIndexTest(TestCase):

    def test_login_required(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PublicManufacturerTest(TestCase):

    def test_login_required(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test-bmw")
        Manufacturer.objects.create(name="test-tusla")
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        manufacturer = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturer))

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):

    def test_login_required(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer1 = Manufacturer.objects.create(
            name="test1", country="test2")
        manufacturer2 = Manufacturer.objects.create(
            name="test2", country="test2")
        Car.objects.create(model="test-X8", manufacturer=manufacturer1)
        Car.objects.create(model="test-Range", manufacturer=manufacturer2)
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        car = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]),
                         list(car))

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_toggle_car_driver_by_current_user(self):
        manufacturer1 = Manufacturer.objects.create(
            name="test1", country="test2")
        car = Car.objects.create(model="test-X8", manufacturer=manufacturer1)
        url = reverse("taxi:car-detail", args=[car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url_toggle = reverse("taxi:toggle-car-assign", args=[car.id])

        # toggle-car-assign ON
        response = self.client.get(url_toggle)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(list(car.drivers.all()),
                         list(get_user_model().objects.all()))

        # toggle-car-assign OFF
        response = self.client.get(url_toggle)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(list(car.drivers.all()), [])


class PublicDriverTest(TestCase):

    def test_login_required(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Driver.objects.create(
            username="test-user",
            password="test123passw",
            license_number="TST12345",
            first_name="Test_first1",
            last_name="Test_last1"
        )
        Driver.objects.create(
            username="test-user2",
            password="test123passw2",
            license_number="TST22345",
            first_name="Test_first2",
            last_name="Test_last2"
        )
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        driver = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]),
                         list(driver))

        self.assertTemplateUsed(response, "taxi/driver_list.html")
