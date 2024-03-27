from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicViewsTests(TestCase):
    def test_index_view_login_required(self) -> None:
        url = reverse("taxi:index")
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_list_view_login_required(self) -> None:
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_create_view_login_required(self) -> None:
        url = reverse("taxi:manufacturer-create")
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_update_view_login_required(self) -> None:
        url = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_delete_view_login_required(self) -> None:
        url = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_car_list_view_login_required(self) -> None:
        url = reverse("taxi:car-list")
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_car_detail_view_login_required(self) -> None:
        url = reverse("taxi:car-detail", kwargs={"pk": 1})
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_car_create_view_login_required(self) -> None:
        url = reverse("taxi:car-create")
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_car_update_view_login_required(self) -> None:
        url = reverse("taxi:car-update", kwargs={"pk": 1})
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_car_delete_view_login_required(self) -> None:
        url = reverse("taxi:car-delete", kwargs={"pk": 1})
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_driver_list_view_login_required(self) -> None:
        url = reverse("taxi:driver-list")
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_driver_detail_view_login_required(self) -> None:
        url = reverse("taxi:driver-detail", kwargs={"pk": 1})
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_driver_create_view_login_required(self) -> None:
        url = reverse("taxi:driver-create")
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_driver_license_update_view_login_required(self) -> None:
        url = reverse("taxi:driver-update", kwargs={"pk": 1})
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)

    def test_driver_delete_view_login_required(self) -> None:
        url = reverse("taxi:driver-delete", kwargs={"pk": 1})
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)


class PrivateViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="test12345",
            license_number="ABC12345"
        )

        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Ferrari", country="Italy")

        self.manufacturers = Manufacturer.objects.all()

        Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturers.get(name="Ford")
        )
        Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturers.get(name="Ford")
        )

        self.cars = Car.objects.all()

        get_user_model().objects.create_user(
            username="first.driver",
            password="test12345",
            license_number="ABC11111"
        )
        get_user_model().objects.create_user(
            username="second.driver",
            password="test12345",
            license_number="ABC22222"
        )

        self.drivers = get_user_model().objects.all()

    def test_retrieve_manufacturers(self) -> None:
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(self.manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturers_with_search(self) -> None:
        name = "Ford"
        searched_manufacturers = self.manufacturers.filter(name=name)

        query_params = {"name": name}
        url = reverse("taxi:manufacturer-list") + "?" + urlencode(query_params)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(searched_manufacturers)
        )

    def test_retrieve_manufacturer_to_update(self) -> None:
        manufacturer = self.manufacturers.get(name="Ford")

        url = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": manufacturer.pk}
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["object"], manufacturer)
        self.assertTemplateUsed(res, "taxi/manufacturer_form.html")

    def test_retrieve_cars(self) -> None:
        url = reverse("taxi:car-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["car_list"]), list(self.cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_retrieve_cars_with_search(self) -> None:
        model = "Mustang"
        searched_cars = self.cars.filter(model__icontains=model)

        query_params = {"model": model}
        url = reverse("taxi:car-list") + "?" + urlencode(query_params)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["car_list"]), list(searched_cars))

    def test_retrieve_car_detail(self) -> None:
        car = self.cars.get(model="Mustang")

        url = reverse("taxi:car-detail", kwargs={"pk": car.pk})
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["object"], car)
        self.assertTemplateUsed(res, "taxi/car_detail.html")

    def test_retrieve_car_to_update(self) -> None:
        car = self.cars.get(model="Mustang")

        url = reverse("taxi:car-update", kwargs={"pk": car.pk})
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["object"], car)
        self.assertTemplateUsed(res, "taxi/car_form.html")

    def test_retrieve_drivers(self) -> None:
        url = reverse("taxi:driver-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(self.drivers))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_retrieve_drivers_with_search(self) -> None:
        username = "first"
        searched_drivers = self.drivers.filter(username__icontains=username)

        query_params = {"username": username}
        url = reverse("taxi:driver-list") + "?" + urlencode(query_params)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(searched_drivers)
        )

    def test_retrieve_driver_detail(self) -> None:
        driver = self.drivers.get(username="first.driver")

        url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["object"], driver)
        self.assertTemplateUsed(res, "taxi/driver_detail.html")

    def test_retrieve_driver_license_to_update(self) -> None:
        driver = self.drivers.get(username="first.driver")

        url = reverse("taxi:driver-update", kwargs={"pk": driver.pk})
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["object"], driver)
        self.assertTemplateUsed(res, "taxi/driver_form.html")
