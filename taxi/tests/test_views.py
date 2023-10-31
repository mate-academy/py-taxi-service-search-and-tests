from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")

paginated_by = 5


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test"
        )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpass123",
            license_number="ABC123455",
        )
        self.car = Car.objects.create(
            model="TestCar",
            manufacturer=self.manufacturer
        )

    def test_toggle_assign_to_car(self) -> None:
        self.assertFalse(self.car.drivers.filter(id=self.user.id).exists())
        self.car.drivers.add(self.user)
        self.car.save()
        self.assertTrue(self.car.drivers.filter(id=self.user.id).exists())
        self.car.drivers.remove(self.user)
        self.car.save()
        self.assertFalse(self.car.drivers.filter(id=self.user.id).exists())
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_toggle_assign_to_car_when_not_logged_in(self) -> None:
        self.assertFalse(self.car.drivers.exists())
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("taxi:toggle-car-assign", args=[self.car.pk]),
        )
        self.assertFalse(self.car.drivers.exists())


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpass123",
            license_number="ABC123455",
        )
        for i in range(8):
            get_user_model().objects.create(
                username=f"user_{i}",
                password=f"pass_{i}",
                license_number=f"ABC1234{i}",
            )
        self.client.force_login(self.user)

    def test_retrieve_driver(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEquals(response.status_code, 200)
        driver = Driver.objects.all()
        self.assertEquals(
            list(response.context["driver_list"]),
            list(driver)[:paginated_by],
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_username(self) -> None:
        searched_username = "user_4"
        response = self.client.get(
            DRIVER_LIST_URL,
            {"username": searched_username}
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.context["driver_list"][0].username,
            searched_username,
        )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpass123",
            license_number="ABC123455",
        )
        for i in range(15):
            manufacturer = Manufacturer.objects.create(
                name=f"manf_name_{i}", country=f"manf_country_{i}"
            )
            Car.objects.create(
                model=f"model_{i}",
                manufacturer=manufacturer,
            )
        self.client.force_login(self.user)

    def test_retrieve_car(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        self.assertEquals(response.status_code, 200)
        car = Car.objects.all()
        self.assertEquals(
            list(response.context["car_list"]),
            list(car)[:paginated_by],
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car_by_model(self) -> None:
        searched_model = "model_8"
        response = self.client.get(CAR_LIST_URL, {"model": searched_model})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.context["car_list"][0].model,
            searched_model
        )


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpass123",
            license_number="ABC123455",
        )
        for i in range(15):
            Manufacturer.objects.create(
                name=f"name_{i}",
                country=f"country_{i}"
            )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEquals(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturer)[:paginated_by],
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self) -> None:
        searched_name = "name_8"
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": searched_name}
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.context["manufacturer_list"][0].name,
            searched_name,
        )


class AccessControlTestTest(TestCase):
    def assert_access_control(self, url_name) -> None:
        res = self.client.get(url_name)
        self.assertNotEquals(res.status_code, 200)
        self.assertRedirects(res, f"/accounts/login/?next={url_name}")

    def test_manufacturer_login_required(self) -> None:
        self.assert_access_control(MANUFACTURER_LIST_URL)

    def test_car_login_required(self) -> None:
        self.assert_access_control(CAR_LIST_URL)

    def test_driver_login_required(self) -> None:
        self.assert_access_control(DRIVER_LIST_URL)
