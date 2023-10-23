from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="FCQ",
            country="Poland",
        )
        Manufacturer.objects.create(
            name="KDLS",
            country="Germany",
        )
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicDriverTest(TestCase):
    def test_login_required_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_detail(self):
        driver = get_user_model().objects.create(
            username="leo.messi",
            password="leomessipassword",
            first_name="Lionel",
            last_name="Messi",
        )
        detail_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        res = self.client.get(detail_url)
        self.assertNotEquals(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create(
            username="leo.messi",
            password="leomessipassword",
            first_name="Lionel",
            last_name="Messi",
            license_number="sadadas"
        )
        get_user_model().objects.create(
            username="frenkie22",
            password="fren22",
            first_name="Frenkie",
            last_name="De Jong",
            license_number="qwrsfs"
        )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PublicCarTest(TestCase):
    def test_login_required_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_detail(self):
        manufacturer = Manufacturer.objects.create(
            name="FCQ",
            country="Poland",
        )

        car = Car.objects.create(
            model="SP250",
            manufacturer=manufacturer,
        )
        detail_url = reverse("taxi:car-detail", kwargs={"pk": car.pk})
        res = self.client.get(detail_url)
        self.assertNotEquals(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        manufacturer = Manufacturer.objects.create(
            name="FCQ",
            country="Poland",
        )

        Car.objects.create(
            model="SP250",
            manufacturer=manufacturer,
        )
        manufacturer2 = Manufacturer.objects.create(
            name="FPODG",
            country="Ukraine",
        )
        Car.objects.create(
            model="SUJWN",
            manufacturer=manufacturer2,
        )

        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.driver = get_user_model().objects.create(
            username="leo.messi",
            password="leomessipassword",
            first_name="Lionel",
            last_name="Messi",
            license_number="sadadas"
        )
        manufacturer = Manufacturer.objects.create(
            name="FCQ",
            country="Poland",
        )

        self.car = Car.objects.create(
            model="SP250",
            manufacturer=manufacturer,
        )

    def test_toggle_assign_to_car_toggle_on(self):
        self.driver.cars.add(self.car)
        self.assertTrue(self.driver.cars.filter(id=self.car.id).exists())

    def test_toggle_assign_to_car_toggle_off(self):
        self.driver.cars.remove(self.car)
        self.assertFalse(self.driver.cars.filter(id=self.car.id).exists())
