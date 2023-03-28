from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Car, Manufacturer, Driver


class PublicViewTest(TestCase):
    def test_login_required_index(self):
        result = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(result.status_code, 200)

    def test_login_required_manufacturer_list_view(self):
        result = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(result.status_code, 200)

    def test_login_required_car_list_view(self):
        result = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(result.status_code, 200)

    def test_login_required_car_detail_view(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        car = Car.objects.create(model="TestModel", manufacturer=manufacturer)
        result = self.client.get(reverse("taxi:car-detail", args=[car.id]))
        self.assertNotEqual(result.status_code, 200)

    def test_login_required_driver_list_view(self):
        result = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(result.status_code, 200)

    def test_login_required_driver_detail_view(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="12345",
            first_name="first_test",
            last_name="last_test",
        )
        result = self.client.get(
            reverse("taxi:driver-detail", args=[driver.id])
        )
        self.assertNotEqual(result.status_code, 200)


class PrivateViewManufacturerTest(TestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="test",
            password="12345",
            first_name="first_test",
            last_name="last_test",
        )
        self.client.force_login(user=user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="TestName1", country="TestCountry")
        Manufacturer.objects.create(name="TestName2", country="TestCountry")
        manufacturer_list = Manufacturer.objects.all()
        result = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(
            list(result.context["manufacturer_list"]), list(manufacturer_list)
        )
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, "taxi/manufacturer_list.html")

    def test_manufacturer_search_form_in_context(self):
        result = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(result.status_code, 200)
        self.assertTrue("search_form" in result.context)
        self.assertIsInstance(
            result.context["search_form"], ManufacturerSearchForm
        )

    def test_manufacturer_list_search(self):
        Manufacturer.objects.create(name="TestName", country="TestCountry")
        Manufacturer.objects.create(name="XXXX", country="TestCountry")
        manufacturer_list = Manufacturer.objects.filter(name__icontains="XXXX")
        result = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "XXXX"}
        )
        self.assertEqual(result.status_code, 200)
        self.assertTrue("manufacturer_list" in result.context)
        self.assertEqual(
            list(result.context["manufacturer_list"]), list(manufacturer_list)
        )


class PrivateViewCarTest(TestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="test",
            password="12345",
            first_name="first_test",
            last_name="last_test",
        )
        self.client.force_login(user=user)

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        Car.objects.create(model="TestModel", manufacturer=manufacturer)
        car_list = Car.objects.all()
        result = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(list(result.context["car_list"]), list(car_list))
        self.assertTemplateUsed(result, "taxi/car_list.html")

    def test_car_search_form_in_context(self):
        result = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(result.status_code, 200)
        self.assertTrue("search_form" in result.context)
        self.assertIsInstance(result.context["search_form"], CarSearchForm)

    def test_car_list_search(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        Car.objects.create(model="TestModel", manufacturer=manufacturer)
        Car.objects.create(model="XXXX", manufacturer=manufacturer)
        car_list = Car.objects.filter(model__icontains="XXXX")
        result = self.client.get(reverse("taxi:car-list"), {"model": "XXXX"})
        self.assertEqual(result.status_code, 200)
        self.assertTrue("car_list" in result.context)
        self.assertEqual(list(result.context["car_list"]), list(car_list))


class PrivateViewDriverTest(TestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="test",
            password="12345",
            first_name="first_test",
            last_name="last_test",
        )
        self.client.force_login(user=user)

    def test_retrieve_driver_list(self):
        result = self.client.get(reverse("taxi:driver-list"))
        driver_list = Driver.objects.all()
        self.assertTemplateUsed(result, "taxi/driver_list.html")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            list(result.context["driver_list"]), list(driver_list)
        )
        self.assertTemplateUsed(result, "taxi/driver_list.html")

    def test_driver_search_form_in_context(self):
        result = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(result.status_code, 200)
        self.assertTrue("search_form" in result.context)
        self.assertIsInstance(result.context["search_form"], DriverSearchForm)

    def test_driver_list_search(self):
        get_user_model().objects.create_user(
            username="XXXX", password="123456", license_number="ABC12345"
        )
        driver_list = Driver.objects.filter(username__icontains="XXXX")
        result = self.client.get(
            reverse("taxi:driver-list"), {"username": "XXXX"}
        )
        self.assertEqual(result.status_code, 200)
        self.assertTrue("driver_list" in result.context)
        self.assertEqual(
            list(result.context["driver_list"]), list(driver_list)
        )
