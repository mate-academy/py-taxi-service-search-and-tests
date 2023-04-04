from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class TestCarSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver1",
            first_name="test_first_name1",
            last_name="test_last_name1",
            password="test_password1",
            license_number="BAC12345",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        Car.objects.create(
            model="car1_test", manufacturer=manufacturer
        )
        Car.objects.create(
            model="car2_test", manufacturer=manufacturer
        )
        Car.objects.create(
            model="car3_test", manufacturer=manufacturer
        )

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=r1"
        )
        cars = Car.objects.filter(model__icontains="car1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))


class TestDriverSearch(TestCase):
    def setUp(self):

        self.driver1 = Driver.objects.create(
            username="test_driver1",
            first_name="test_first_name1",
            last_name="test_last_name1",
            password="test_password1",
            license_number="BAC12345",
        )
        self.driver2 = Driver.objects.create(
            username="test_driver2",
            first_name="test_first_name2",
            last_name="test_last_name2",
            password="test_password2",
            license_number="BBC12345",
        )
        self.driver3 = Driver.objects.create(
            username="test_driver3",
            first_name="test_first_name3",
            last_name="test_last_name3",
            password="test_password3",
            license_number="BBB12345",
        )
        self.client.force_login(self.driver1)

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=ver3"
        )
        drivers = get_user_model().objects.filter(
            username__icontains="driver3"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))


class PublicManufacturerTest(TestCase):
    def test_list_manufacturers(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_list_drivers(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_driver_detail(self):
        res = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_list_cars(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_car_detail(self):
        res = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="test_password1",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response, "taxi/manufacturer_list.html"
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="test_password1",
            license_number="BAC12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="test_password1",
            license_number="BAC12345",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.get(name="test_manufacturer")
        )

    def test_retrieve_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
