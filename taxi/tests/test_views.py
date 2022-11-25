from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required_list(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_create(self) -> None:
        response = self.client.get(MANUFACTURER_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="billy.hargrove",
            password="pro12345",
            first_name="Billy",
            last_name="Hargrove",
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturers(self) -> None:
        Manufacturer.objects.create(
            name="FCA", country="Italy",
        )
        Manufacturer.objects.create(
            name="BMW", country="Germany",
        )

        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_login_required_update(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany",
        )
        manufacturer_update_url = reverse(
            "taxi:manufacturer-update", args=[manufacturer.pk],
        )
        response = self.client.post(manufacturer_update_url)
        self.assertEqual(response.status_code, 200)

    def test_login_required_deleted(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany",
        )
        manufacturer_delete_url = reverse(
            "taxi:manufacturer-delete", args=[manufacturer.pk],
        )
        response = self.client.post(manufacturer_delete_url)
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_type_search(self) -> None:
        search_form = "BMW"
        manufacturer_search = Manufacturer.objects.create(
            name=search_form, country="Germany",
        )
        manufacturers = (
            {"model": "Beijing EX5", "country": "China"},
            {"model": "Ford Focus", "country": "USA"},
            {"model": "SP250", "country": "Germany"},
            {"model": "Rising Auto ER6", "country": "China"},
            {"model": "MX-30", "country": "Japan"},
        )
        for manufacturer in manufacturers:
            Manufacturer.objects.create(
                name=manufacturer["model"], country=manufacturer["country"],
            )
        response = self.client.get(
            f"{MANUFACTURER_LIST_URL}?name={search_form}",
        )

        self.assertEqual(
            response.context["manufacturer_list"].count(), 1,
        )
        self.assertEqual(
            response.context["manufacturer_list"][0], manufacturer_search,
        )


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="some.user", password="pro12345",
        )
        self.client.force_login(self.user)

    def test_create_driver(self) -> None:
        form_data = {
            "username": "jim.hopper",
            "password1": "bobo7657",
            "password2": "bobo7657",
            "license_number": "JIM26531",
            "first_name": "Jim",
            "last_name": "Hopper",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"],
        )

        self.assertEqual(
            new_driver.first_name, form_data["first_name"],
        )
        self.assertEqual(
            new_driver.last_name, form_data["last_name"],
        )
        self.assertEqual(
            new_driver.license_number, form_data["license_number"],
        )


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="bla.blabla",
            password="dkdiek13",
            first_name="Bla",
            last_name="Blabla",
        )
        self.client.force_login(self.driver)

    def test_retrieve_cars(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany",
        )
        Car.objects.create(
            model="BMW i7", manufacturer=manufacturer,
        )
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]), list(cars),
        )
        self.assertTemplateUsed(
            response, "taxi/car_list.html",
        )

    def test_login_required_update(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany",
        )
        car = Car.objects.create(
            model="BMW i7", manufacturer=manufacturer,
        )
        car_update_url = reverse(
            "taxi:car-update", args=[car.pk],
        )
        response = self.client.post(car_update_url)
        self.assertEqual(response.status_code, 200)

    def test_login_required_deleted(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany",
        )
        car = Car.objects.create(
            model="BMW i7", manufacturer=manufacturer,
        )
        car_delete_url = reverse("taxi:car-delete", args=[car.pk])
        response = self.client.post(car_delete_url)

        self.assertEqual(response.status_code, 302)

    def test_car_search(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Lincoln", country="USA",
        )
        search_form = "Mitsubishi Eclipse"
        car_search = Car.objects.create(
            model=search_form, manufacturer=manufacturer,
        )
        cars = (
            "Beijing EX5",
            "Ford Focus",
            "SP250",
            "Rising Auto ER6",
            "MX-30",
        )
        for car in cars:
            Car.objects.create(
                model=car, manufacturer=manufacturer,
            )
        response = self.client.get(f"{CAR_LIST_URL}?model={search_form}")

        self.assertEqual(
            response.context["car_list"].count(), 1,
        )
        self.assertEqual(
            response.context["car_list"][0], car_search,
        )
