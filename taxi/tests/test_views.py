from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car

HOME_PAGE_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicHomePage(TestCase):
    def test_login_required(self):
        res = self.client.get(HOME_PAGE_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateHomePage(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="password1234", license_number="QWE12345"
        )
        self.client.force_login(self.user)

    def test_home_page(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Ukraine"
        )
        Car.objects.create(model="ZAZ Lanos", manufacturer=manufacturer)

        num_cars = Car.objects.count()
        num_drivers = get_user_model().objects.count()
        num_manufacturers = Manufacturer.objects.count()

        res = self.client.get(HOME_PAGE_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["num_drivers"], num_drivers)
        self.assertEqual(res.context["num_cars"], num_cars)
        self.assertEqual(res.context["num_manufacturers"], num_manufacturers)
        self.assertTemplateUsed(res, "taxi/index.html")


class PublicManufacturerTests(TestCase):
    def test_login_required_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test2",
            password="password12345",
            license_number="CXZ12345"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list(self):
        Manufacturer.objects.create(name="test", country="Ukraine")
        Manufacturer.objects.create(name="another_test", country="USA")

        res = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        response = self.client.get(MANUFACTURER_LIST_URL + "?name=Ford")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="Ford")
        )


class PublicDriverTests(TestCase):
    def test_login_required_driver_list(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_detail(self):
        user = get_user_model().objects.create_user(
            username="test", password="test12345", license_number="ZXC21345"
        )
        res = self.client.get(reverse("taxi:driver-detail", args=[user.id]))

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="password1234", license_number="QWE12345"
        )
        self.client.force_login(self.user)

    def test_driver_list(self):
        self.user = get_user_model().objects.create_user(
            username="IVAN", password="qwerty123", license_number="IOP09876"
        )
        drivers = get_user_model().objects.all()
        res = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_driver_detail(self):
        res = self.client.get(reverse(
            "taxi:driver-detail",
            args=[self.user.id])
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["driver"], self.user)
        self.assertTemplateUsed(res, "taxi/driver_detail.html")

    def test_driver_create(self):
        form_data = {
            "username": "test",
            "password1": "password1234",
            "password2": "password1234",
            "first_name": "Ivan",
            "last_name": "Drago",
            "license_number": "QWE12345",
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)
        user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(user.license_number, form_data["license_number"])


class CarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )

    def test_create_car(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Continental",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Car.objects.get(id=self.user.cars.first().id).model, "Continental"
        )

    def test_update_car(self):
        car = Car.objects.create(
            model="Continental",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": car.id}),
            {
                "pk": car.id,
                "model": "Not Continental",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        Car.objects.get(id=car.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.get(id=car.id).model, "Not Continental")

    def test_delete_car(self):
        car = Car.objects.create(
            model="Continental",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())
