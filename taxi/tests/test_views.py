from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

HOME_PAGE_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicHomePageTests(TestCase):
    def test_login_required(self):
        res = self.client.get(HOME_PAGE_URL)

        self.assertEqual(res.status_code, 302)


class PrivateHomePageTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="testuser12345",
            license_number="QWE12345"
        )
        self.client.force_login(self.driver)

    def test_home_page(self):
        manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(model="DMW x6", manufacturer=manufacturer)

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

        self.assertEqual(res.status_code, 302)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="testuser12345",
            license_number="QWE12345"
        )
        self.client.force_login(self.driver)

    def test_manufacturers_list(self):
        for i in range(5):
            Manufacturer.objects.create(
                name=f"car manufacturer - {i}",
                country=f"country - {i}"
            )

        manufacturers = Manufacturer.objects.all()

        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_manufacturer_create(self):
        form_data = {
            "name": "BMW",
            "country": "Germany"
        }
        self.client.post(MANUFACTURER_CREATE_URL, data=form_data)
        manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(manufacturer.name, form_data["name"])
        self.assertEqual(manufacturer.country, form_data["country"])

    def test_manufacturer_update(self):
        manufacturer = Manufacturer.objects.create(name="Audi", country="Germany")
        manufacturer_id = manufacturer.id

        form_data = {
            "name": "ZAZ",
            "country": "Ukraine"
        }

        self.client.post(reverse(
            "taxi:manufacturer-update", args=[manufacturer_id]
        ), data=form_data)

        updated_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(updated_manufacturer.id, manufacturer_id)
        self.assertEqual(updated_manufacturer.name, form_data["name"])
        self.assertEqual(updated_manufacturer.country, form_data["country"])

    def test_manufacturer_search(self):
        manufacturer_name = "to_search"
        manufacturer_to_search = Manufacturer.objects.create(
            name=manufacturer_name,
            country="Ukraine"
        )
        for i in range(5):
            Manufacturer.objects.create(
                name=f"some_manufacturer_{i}",
                country="Japan"
            )

        res = self.client.get(f"{MANUFACTURER_LIST_URL}?name={manufacturer_name}")

        self.assertEqual(len(res.context["manufacturer_list"]), 1)

        self.assertEqual(
            res.context["manufacturer_list"][0],
            manufacturer_to_search
        )


class PublicCarListView(TestCase):
    def test_car_list_login_required_(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertEqual(res.status_code, 302)

    def test_car_detail_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name=f"car manufacturer",
            country=f"country"
        )
        car = Car.objects.create(
            model="car model",
            manufacturer=manufacturer
        )

        res = self.client.get(reverse("taxi:car-detail", args=[car.pk]))

        self.assertEqual(res.status_code, 302)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="testuser12345",
            license_number="QWE12345"
        )
        self.client.force_login(self.driver)

    def test_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name=f"car manufacturer",
            country=f"country"
        )
        for i in range(5):
            Car.objects.create(
                model=f"car model - {i}",
                manufacturer=manufacturer
            )

        cars = Car.objects.all()

        res = self.client.get(CAR_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_car_detail(self):
        manufacturer = Manufacturer.objects.create(
            name=f"car manufacturer",
            country=f"country"
        )
        car = Car.objects.create(
            model=f"BMW x5",
            manufacturer=manufacturer,
        )
        car.drivers.add(self.driver)

        res = self.client.get(reverse("taxi:car-detail", args=[car.pk]))
        print(res.context)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["car"], car)
        self.assertTemplateUsed(res, "taxi/car_detail.html")

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="Ukraine"
        )
        car_model = "to_search"
        car_to_search = Car.objects.create(
            model=car_model,
            manufacturer=manufacturer
        )

        for i in range(5):
            Car.objects.create(
                model=f"some_car_{i}",
                manufacturer=manufacturer
            )

        res = self.client.get(f"{CAR_LIST_URL}?model={car_model}")

        self.assertEqual(len(res.context["car_list"]), 1)

        self.assertEqual(
            res.context["car_list"][0],
            car_to_search
        )


class PublicDriverTests(TestCase):
    def test_driver_list_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(res.status_code, 302)

    def test_driver_detail_login_required(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="user12345",
            license_number="QWE12345"
        )
        res = self.client.get(reverse("taxi:driver-detail", args=[user.id]))

        self.assertEqual(res.status_code, 302)


class PrivateDroverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="user12345",
            license_number="QWE12345"
        )

        self.client.force_login(self.driver)

    def test_driver_list(self):
        for i in range(1, 5):
            self.driver = get_user_model().objects.create_user(
                username=f"test_user_{i}",
                password="testuser12345",
                license_number=f"QWE1234{i}"
            )
        drivers = get_user_model().objects.all()
        res = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_driver_detail(self):
        res = self.client.get(reverse("taxi:driver-detail", args=[self.driver.pk]))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["driver"], self.driver)
        self.assertTemplateUsed(res, "taxi/driver_detail.html")

    def test_driver_create(self):
        form_data = {
            "username": "test_user",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "QWE12345"
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)

        user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(user.license_number, form_data["license_number"])
