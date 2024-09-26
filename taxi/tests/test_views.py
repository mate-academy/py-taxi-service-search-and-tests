from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver
from taxi.views import ManufacturerListView


def create_new_user_setup(obj):
    obj.user = get_user_model().objects.create_user(
        username="test_username", password="test_password"
    )

    obj.client.force_login(obj.user)


class PublicTest(TestCase):
    def test_login_required_for_main_pages(self):
        self.assertNotEqual(self.client.get(reverse("taxi:car-list")), 200)
        self.assertNotEqual(
            self.client.get(reverse("taxi:manufacturer-list")), 200
        )
        self.assertNotEqual(self.client.get(reverse("taxi:driver-list")), 200)
        self.assertNotEqual(self.client.get(reverse("taxi:index")), 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        create_new_user_setup(self)
        for char in range(5):
            Manufacturer.objects.create(
                name=f"test_name{char}", country=f"test_country{char}"
            )

    def test_retrieve_manufacturers_list(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturer_list = Manufacturer.objects.all()

        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturer_list)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_manufacturer_list_page_have_pagination(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(
            len(res.context["manufacturer_list"]),
            ManufacturerListView.paginate_by,
        )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        create_new_user_setup(self)

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        Car.objects.create(model="test_model1", manufacturer=manufacturer)
        Car.objects.create(model="test_model2", manufacturer=manufacturer)

        car_list = Car.objects.all()
        res = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(list(res.context["car_list"]), list(car_list))
        self.assertTemplateUsed(res, "taxi/car_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        create_new_user_setup(self)

    def test_retrieve_driver_list(self):
        for i in range(3):
            Driver.objects.create_user(
                username=f"username1{i}", password="password12"
            )

        driver_list = Driver.objects.all()
        res = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(list(res.context["driver_list"]), list(driver_list))
        self.assertTemplateUsed(res, "taxi/driver_list.html")
