from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": 1})
CAR_DELETE_URL = reverse("taxi:car-delete", kwargs={"pk": 1})

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", kwargs={"pk": 1})
DRIVER_DELETE_URL = reverse("taxi:driver-delete", kwargs={"pk": 1})


class PublicManufacturerTest(TestCase):
    def test_login_required_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_create(self):
        res = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_update(self):
        res = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_delete(self):
        res = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Manufacturer_1")
        Manufacturer.objects.create(name="Manufacturer_2")

    def test_retrieve_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_search(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "1"})
        manufacturer = Manufacturer.objects.filter(name__icontains="1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )

    def test_retrieve_manufacturer_create(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_retrieve_manufacturer_update(self):
        response = self.client.get(MANUFACTURER_UPDATE_URL)
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(response.context["manufacturer"], manufacturer)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_retrieve_manufacturer_delete(self):
        response = self.client.get(MANUFACTURER_DELETE_URL)
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(response.context["manufacturer"], manufacturer)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )


class PublicCarTest(TestCase):
    def test_login_required_car_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_detail(self):
        res = self.client.get(CAR_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_create(self):
        res = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_update(self):
        res = self.client.get(CAR_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_delete(self):
        res = self.client.get(CAR_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Manufacturer_1",
        )
        Car.objects.create(model="Car_1", manufacturer=manufacturer)
        Car.objects.create(model="Car_2", manufacturer=manufacturer)

    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_search(self):
        response = self.client.get(CAR_LIST_URL, {"model": "1"})
        car = Car.objects.filter(model__icontains="1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(car))

    def test_retrieve_car_detail(self):
        response = self.client.get(CAR_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        car = Car.objects.get(id=1)
        self.assertEqual(response.context["car"], car)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_retrieve_car_create(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_retrieve_car_update(self):
        response = self.client.get(CAR_UPDATE_URL)
        car = Car.objects.get(id=1)
        self.assertEqual(response.context["car"], car)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_retrieve_car_delete(self):
        response = self.client.get(CAR_DELETE_URL)
        car = Car.objects.get(id=1)
        self.assertEqual(response.context["car"], car)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")


class PublicDriverTest(TestCase):
    def test_login_required_driver_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_detail(self):
        res = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_create(self):
        res = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_update(self):
        res = self.client.get(DRIVER_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_delete(self):
        res = self.client.get(DRIVER_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        Driver.objects.create_user(
            username="Driver_1",
            password="test1234",
            license_number="TES12345",
        )
        Driver.objects.create_user(
            username="Driver_2",
            password="test1234",
            license_number="TES56789",
        )

    def test_retrieve_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_driver_list_search(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "1"})
        drivers = Driver.objects.filter(username__icontains="1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_retrieve_driver_detail(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        driver = Driver.objects.get(id=1)

        self.assertEqual(response.context["driver"], driver)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_retrieve_driver_create(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES23456",
        }
        self.client.post(DRIVER_CREATE_URL, form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_retrieve_driver_license_update(self):

        response = self.client.get(DRIVER_UPDATE_URL)
        driver = Driver.objects.get(id=1)
        self.assertEqual(response.context["driver"], driver)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_retrieve_driver_delete(self):
        response = self.client.get(DRIVER_DELETE_URL)
        driver = Driver.objects.get(id=1)

        self.assertEqual(response.context["driver"], driver)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")
