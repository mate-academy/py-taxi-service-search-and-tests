from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class TestDriverListPublic(TestCase):

    def test_login_required(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)


class TestDriverListPrivate(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user12345"
        )
        self.url = reverse("taxi:driver-create")
        self.client.force_login(self.user)
        self.driver = Driver.objects.create(
            username="test",
            password="testtesttesttest",
            license_number="AAA18345"
        )

    def test_private_presentation_driver_list(self):
        Driver.objects.create(
            license_number="AAA12345"
        )
        res = self.client.get(reverse("taxi:driver-list"))
        driver = Driver.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(driver)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_create_driver(self):
        form_driver = {
            "username": "nick",
            "password1": "abcdefg12345",
            "password2": "abcdefg12345",
            "email": "aaa@ff.com",
            "first_name": "Jo",
            "last_name": "Bush",
            "license_number": "AAA12345"
        }
        url = reverse("taxi:driver-create")
        self.client.post(url, data=form_driver)

        new_driver = get_user_model().objects.get(
            username=form_driver["username"]
        )
        self.assertEqual(
            new_driver.first_name,
            form_driver["first_name"]
        )
        self.assertEqual(
            new_driver.license_number,
            form_driver["license_number"]
        )


class TestManufacturerPublic(TestCase):

    def test_public_not_presentation_page_manufacturer_list(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        self.assertNotEqual(response.status_code, 200)


class TestManufacturerPrivate(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_private_presentation_manufacturer_list(self):
        Manufacturer.objects.create(
            name="Ford",
            country="Germany"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class TestCarPublic(TestCase):

    def test_public_presentation_page_car_list(self):
        response = self.client.get(
            reverse("taxi:car-list")
        )
        self.assertNotEqual(response.status_code, 200)


class TestCarPrivate(TestCase):

    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer
        )

        self.user = get_user_model().objects.create_user(
            username="Bo",
            password="bo12345"
        )
        self.client.force_login(self.user)

    def test_private_presentation_page_car_list(self):

        response = self.client.get(
            reverse("taxi:car-list")
        )
        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
