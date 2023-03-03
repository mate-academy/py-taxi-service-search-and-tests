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
        self.client.login(
            username="user",
            password="user12345"
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
            "password1": "12345",
            "password2": "12345",
            "first_name": "Jo",
            "last_name": "Bush",
            "license_1number": "AAA12345"
        }
        url = reverse("taxi:driver-create")
        self.client.post(url, data=form_driver)
        print("!!!!!!!!!!!!!!!!!!!!!!!POST!!!!!!!!!!!!!!!!!!!!!")

        new_driver = get_user_model().objects.get(username=form_driver["username"])
        print("!!!!!!!!!!!!!!!!!!!!!!!NEWDRIVER!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.assertEqual(new_driver.first_name, form_driver["first_name"])

    # def test_delete_driver(self):
    #     driver = get_user_model().objects.create(
    #         username="bob",
    #         first_name="name",
    #         last_name="name2",
    #         license_number="AAA12345",
    #         password="123455522hjhg"
    #     )
    #     response = self.client.post(
    #         reverse("taxi:driver-delete", kwargs={"pk": driver.pk})
    #     )
    #     drivers = get_user_model().objects.filter(pk=driver.pk)
    #     self.assertEqual(drivers.count(),0)
    #     self.assertEqual(response.status_code, 302)


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
        self.user = get_user_model().objects.create_user(
            username="Bo",
            password="bo12345"
        )
        self.client.force_login(self.user)

    def test_private_presentation_page_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="Germany"
        )
        Car.objects.create(
            model="Focus",
            manufacturer=manufacturer
        )
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
