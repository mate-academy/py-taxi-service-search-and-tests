from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self) -> None:
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user", password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self) -> None:
        Manufacturer.objects.create(name="Toyota", country="Japan")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class CarDetailsViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user", password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_details(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Corolla", manufacturer=manufacturer)
        url = reverse("taxi:car-detail", args=[car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], car)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class ManufacturerListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="user", password="test1234"
        )
        self.client.force_login(self.user)

    def test_search_manufacturers_list_view_without_filter(self) -> None:
        Manufacturer.objects.create(name="Toyota", country="Japan")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturers_list_view_with_filter(self) -> None:
        Manufacturer.objects.create(name="Toyota", country="Japan")
        url = reverse("taxi:manufacturer-list") + "?name=Toy"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="Toy")),
        )


class DriverListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user", password="test1234", license_number="test123456"
        )
        self.client.force_login(self.user)

    def test_search_driver_list_view_without_filter(self) -> None:
        Driver.objects.create(
            username="driver",
            password="driver123",
            first_name="test_first",
            last_name="test_last",
        )
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]), list(Driver.objects.all())
        )

    def test_search_driver_list_view_with_filter(self) -> None:
        Driver.objects.create(
            username="driver",
            password="driver123",
            first_name="test_first",
            last_name="test_last",
        )
        url = reverse("taxi:driver-list") + "?username=dri"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="dri")),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class CarListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="user", password="test1234"
        )
        self.client.force_login(self.user)

    def test_search_car_list_view_without_filter(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())
        )

    def test_search_car_list_view_with_filter(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        url = reverse("taxi:car-list") + "?model=Cor"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="Cor")),
        )
        self.assertTemplateUsed("taxi/car_list.html")
