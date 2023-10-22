from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
HOME_URL = reverse("taxi:index")


class LoginRequiredViewsTest(TestCase):
    def test_home_page_login_required(self):
        res = self.client.get(HOME_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturers_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_cars_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_drivers_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class RetrieveListsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Subaru", country="Japan")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(name="test_name",
                                                   country="test_country")
        Car.objects.create(model="test_model1", manufacturer=manufacturer)
        Car.objects.create(model="test_model2", manufacturer=manufacturer)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class SearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345"
        )
        self.client.force_login(self.user)

    def test_manufacturer_search(self):
        m1 = Manufacturer.objects.create(name="abc", country="test_country")
        m2 = Manufacturer.objects.create(name="ab", country="test_country")
        Manufacturer.objects.create(name="bc", country="test_country")
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   args={"name": "ab"})
        response_manufacturer_list = list(
            response.context["manufacturer_list"]).sort(key=lambda m: m.id)
        expected_manufacturer_list = [m1, m2].sort(key=lambda m: m.id)

        self.assertEqual(expected_manufacturer_list,
                         response_manufacturer_list)

    def test_car_search(self):
        m1 = Manufacturer.objects.create(name="abc", country="test_country")
        car1 = Car.objects.create(model="ab", manufacturer=m1)
        car2 = Car.objects.create(model="abc", manufacturer=m1)
        Car.objects.create(model="bc", manufacturer=m1)
        response = self.client.get(reverse("taxi:car-list"),
                                   args={"model": "ab"})
        response_car_list = list(
            response.context["car_list"]).sort(key=lambda m: m.id)
        expected_car_list = [car1, car2].sort(key=lambda m: m.id)

        self.assertEqual(expected_car_list,
                         response_car_list)

    def test_driver_search(self):
        driver1 = get_user_model().objects.create_user(
            username="abc",
            password="test1234",
            license_number="AAA00001"
        )
        driver2 = get_user_model().objects.create_user(
            username="ab",
            password="test123445",
            license_number="AAA00002"
        )
        response = self.client.get(reverse("taxi:driver-list"),
                                   args={"username": "ab"})
        response_driver_list = list(
            response.context["driver_list"]).sort(key=lambda m: m.id)
        expected_driver_list = [driver1, driver2].sort(key=lambda m: m.id)

        self.assertEqual(expected_driver_list,
                         response_driver_list)


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self) -> None:
        user = self.user = get_user_model().objects.create_user(
            username="user",
            password="test"
        )
        self.client.force_login(user)
        self.manufacturer = Manufacturer.objects.create(
            name="Subaru",
            country="Japan?"
        )
        self.car = Car.objects.create(
            model="Super expensive and cool one",
            manufacturer=self.manufacturer
        )

    def test_toggle_assign_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        self.client.get(url)
        self.assertIn(self.user, self.car.drivers.all())

        self.client.get(url)
        self.assertNotIn(self.user, self.car.drivers.all())
