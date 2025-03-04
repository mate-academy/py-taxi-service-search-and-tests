from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


URL_MANUFACTURER_LIST = reverse("taxi:manufacturer-list")
URL_CAR_LIST = reverse("taxi:car-list")


class BaseSetUp(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="UniqueTestName",
            password="1qazcde3",
            license_number="AAA11111"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer test",
            country="manufacturer country"
        )
        self.car = Car.objects.create(
            model="Car-test",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.user)


class IsAuthenticatedViewsTests(BaseSetUp):

    def test_index_login_required(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertEqual(res.status_code, 302)

    def test_manufacturer_login_required(self):
        res_list = self.client.get(URL_MANUFACTURER_LIST)
        self.assertEqual(res_list.status_code, 302)

    def test_car_login_required(self):
        res_list = self.client.get(URL_CAR_LIST)
        res_detail = self.client.get(
            reverse("taxi:car-detail", args=[self.car.id])
        )

        self.assertEqual(res_list.status_code, 302)
        self.assertEqual(res_detail.status_code, 302)

    def test_driver_login_required(self):
        res_list = self.client.get(reverse("taxi:driver-list"))
        res_detail = self.client.get(
            reverse("taxi:driver-detail", args=[self.user.id])
        )

        self.assertEqual(res_list.status_code, 302)
        self.assertEqual(res_detail.status_code, 302)

    def test_toggle_assign_login_required(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 302)


class AuthenticatedViewTest(BaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)

    def test_index_status(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertEqual(res.status_code, 200)

    def test_index_context(self):
        url = reverse("taxi:index")
        self.client.get(url)
        res = self.client.get(url)
        self.assertEqual(res.context["num_drivers"], 1)
        self.assertEqual(res.context["num_cars"], 1)
        self.assertEqual(res.context["num_manufacturers"], 1)

        self.assertEqual(res.context["num_visits"], 2)

    def test_index_template(self):
        url = reverse("taxi:index")
        res = self.client.get(url)
        self.assertTemplateUsed(res, "taxi/index.html")

    def test_manufacturer_status(self):
        res = self.client.get(URL_MANUFACTURER_LIST)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_template(self):
        res = self.client.get(URL_MANUFACTURER_LIST)
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        manufacturer2 = Manufacturer.objects.create(
            name="test 2",
            country="test2 country"
        )
        url_1 = URL_MANUFACTURER_LIST + f"?search={manufacturer2.name}"
        res_1 = self.client.get(url_1)
        self.assertContains(res_1, manufacturer2.name)
        self.assertNotContains(res_1, self.manufacturer.name)
        url_2 = URL_MANUFACTURER_LIST + f"?search={self.manufacturer.name}"
        res_2 = self.client.get(url_2)
        self.assertContains(res_2, self.manufacturer.name)
        self.assertNotContains(res_2, manufacturer2.name)
        url_3 = URL_MANUFACTURER_LIST + "?search=test"
        res_3 = self.client.get(url_3)
        self.assertContains(res_3, self.manufacturer.name)
        self.assertContains(res_3, manufacturer2.name)

    def test_car_status(self):
        res = self.client.get(URL_CAR_LIST)
        self.assertEqual(res.status_code, 200)

    def test_car_search(self):
        car2 = Car.objects.create(
            model="UniqueCarModel",
            manufacturer=self.manufacturer
        )
        url_1 = URL_CAR_LIST + f"?search={car2.model}"
        res_1 = self.client.get(url_1)
        self.assertContains(res_1, car2.model)
        self.assertNotContains(res_1, self.car.model)
        url_2 = URL_CAR_LIST + f"?search={self.car.model}"
        res_2 = self.client.get(url_2)
        self.assertContains(res_2, self.car.model)
        self.assertNotContains(res_2, car2.model)
        url_3 = URL_CAR_LIST + "?search=Car"
        res_3 = self.client.get(url_3)
        self.assertContains(res_3, self.car.model)
        self.assertContains(res_3, car2.model)

    def test_driver_status(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(res.status_code, 200)

    def test_toggle_assign_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        self.client.get(url)
        self.assertEqual(self.car.drivers.count(), 0)
        self.client.get(url)
        self.assertEqual(self.car.drivers.count(), 1)
