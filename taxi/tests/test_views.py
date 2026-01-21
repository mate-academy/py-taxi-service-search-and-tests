from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


PAGINATION = 5
ID = 1

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", args=[ID])
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", args=[ID])
CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", args=[ID])
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_DELETE_URL = reverse("taxi:car-delete", args=[ID])
CAR_UPDATE_URL = reverse("taxi:car-update", args=[ID])
CAR_TOGGLE_ASSIGN_URL = reverse("taxi:toggle-car-assign", args=[ID])
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", args=[ID])
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_DELETE_URL = reverse("taxi:driver-delete", args=[ID])
DRIVER_UPDATE_URL = reverse("taxi:driver-update", args=[ID])


class LoginUserMixin(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.get(id=ID)
        self.client.force_login(self.user)


class FixtureMixin(TestCase):
    fixtures = ["taxi/fixtures/taxi_service_db_data.json", ]


class PublicTest(FixtureMixin, TestCase):
    def test_index_login_required(self) -> None:
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_list_login_required(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self) -> None:
        response = self.client.get(CAR_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self) -> None:
        response = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_login_required(self) -> None:
        response = self.client.get(CAR_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self) -> None:
        response = self.client.get(CAR_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_toggle_assign_login_required(self) -> None:
        response = self.client.get(CAR_TOGGLE_ASSIGN_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self) -> None:
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self) -> None:
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_login_required(self) -> None:
        response = self.client.get(DRIVER_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_login_required(self) -> None:
        response = self.client.get(DRIVER_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexTest(LoginUserMixin, FixtureMixin, TestCase):
    def test_count_objects(self) -> None:
        num_drivers = get_user_model().objects.count()
        num_cars = Car.objects.count()
        num_manufacturers = Manufacturer.objects.count()

        response = self.client.get(INDEX_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], num_drivers)
        self.assertEqual(response.context["num_cars"], num_cars)
        self.assertEqual(
            response.context["num_manufacturers"],
            num_manufacturers
        )

    def test_count_visits(self) -> None:
        visits = 5
        for num_visits in range(1, visits + 1):
            response = self.client.get(INDEX_URL)
            self.assertEqual(response.context["num_visits"], num_visits)


class PrivateManufacturerTest(LoginUserMixin, FixtureMixin, TestCase):
    def test_list_pagination_manufacturer(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            PAGINATION
        )

    def test_list_retrieve_data_manufacturer(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()[:PAGINATION]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_search_manufacturer_with_few_results(self) -> None:
        search_str = "to"
        response = self.client.get(
            MANUFACTURER_LIST_URL
            + f"?name={search_str}"
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains=search_str))
        )

    def test_search_manufacturer_with_one_result(self) -> None:
        search_str = "baic"
        response = self.client.get(
            MANUFACTURER_LIST_URL
            + f"?name={search_str}"
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains=search_str))
        )

    def test_search_manufacturer_with_zero_results(self) -> None:
        search_str = "swdeqw"
        response = self.client.get(
            MANUFACTURER_LIST_URL
            + f"?name={search_str}"
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains=search_str))
        )

    def test_create_manufacturer(self) -> None:
        form_data = {
            "name": "Test name",
            "country": "Test country",
        }
        response = self.client.post(MANUFACTURER_CREATE_URL, data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_update_manufacturer(self) -> None:
        form_data = {
            "name": "Test name",
            "country": "Test country"
        }
        response = self.client.post(MANUFACTURER_UPDATE_URL, data=form_data)
        updated_manufacturer = Manufacturer.objects.get(id=ID)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_manufacturer.name, form_data["name"])
        self.assertEqual(updated_manufacturer.country, form_data["country"])

    def test_delete_manufacturer(self) -> None:
        response = self.client.post(MANUFACTURER_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=ID).exists()
        )


class PrivateCarTest(LoginUserMixin, FixtureMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.manufacturer = Manufacturer.objects.get(id=ID)

    def test_list_pagination_car(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(
            len(response.context["car_list"]),
            PAGINATION
        )

    def test_list_retrieve_data_car(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()[:PAGINATION]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_detail_car(self) -> None:
        car = Car.objects.get(id=ID)
        response = self.client.get(CAR_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["car"].model,
            car.model
        )
        self.assertEqual(
            response.context["car"].manufacturer,
            car.manufacturer
        )
        self.assertEqual(
            response.context["car"].drivers,
            car.drivers
        )

    def test_search_car_with_few_results(self) -> None:
        search_str = "mi"
        response = self.client.get(CAR_LIST_URL + f"?model={search_str}")

        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains=search_str))
        )

    def test_search_car_with_one_result(self) -> None:
        search_str = "mitsubishi lancer"
        response = self.client.get(CAR_LIST_URL + f"?model={search_str}")

        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains=search_str))
        )

    def test_search_car_with_zero_results(self) -> None:
        search_str = "wdef"
        response = self.client.get(CAR_LIST_URL + f"?model={search_str}")

        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains=search_str))
        )

    def test_create_car(self) -> None:
        form_data = {
            "model": "Test name",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        response = self.client.post(CAR_CREATE_URL, data=form_data)
        new_car = Car.objects.filter(model=form_data["model"]).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer.id, form_data["manufacturer"])
        self.assertEqual(
            list(new_car.drivers.values_list("id", flat=True)),
            form_data["drivers"]
        )

    def test_update_car(self) -> None:
        form_data = {
            "model": "Test name",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        response = self.client.post(CAR_UPDATE_URL, data=form_data)
        updated_car = Car.objects.get(id=ID)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_car.model, form_data["model"])
        self.assertEqual(
            updated_car.manufacturer.id,
            form_data["manufacturer"]
        )
        self.assertEqual(
            list(updated_car.drivers.values_list("id", flat=True)),
            form_data["drivers"]
        )

    def test_delete_car(self) -> None:
        response = self.client.post(CAR_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Car.objects.filter(id=ID).exists()
        )

    def test_toggle_delete_me(self) -> None:
        car = Car.objects.get(id=ID)
        car.drivers.add(self.user.id)
        car.save()
        self.client.get(CAR_TOGGLE_ASSIGN_URL)
        self.assertNotIn(car, self.user.cars.all())

    def test_toggle_assign_me(self) -> None:
        car = Car.objects.get(id=ID)
        car.drivers.remove(self.user.id)
        car.save()
        self.client.get(CAR_TOGGLE_ASSIGN_URL)
        self.assertIn(car, self.user.cars.all())


class PrivateDriverTest(LoginUserMixin, FixtureMixin, TestCase):
    def test_list_pagination_driver(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(
            len(response.context["driver_list"]),
            PAGINATION
        )

    def test_list_retrieve_data_driver(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        drivers = get_user_model().objects.all()[:PAGINATION]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_detail_driver(self) -> None:
        driver = get_user_model().objects.get(id=ID)
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["driver"].username,
            driver.username
        )
        self.assertEqual(
            response.context["driver"].first_name,
            driver.first_name
        )
        self.assertEqual(
            response.context["driver"].last_name,
            driver.last_name
        )
        self.assertEqual(
            list(response.context["driver"].cars.all()),
            list(driver.cars.all())
        )

    def test_search_driver_with_few_results(self) -> None:
        search_str = "jo"
        response = self.client.get(DRIVER_LIST_URL + f"?username={search_str}")

        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(
                username__icontains=search_str
            ))
        )

    def test_search_driver_with_one_result(self) -> None:
        search_str = "joyce.byers"
        response = self.client.get(DRIVER_LIST_URL + f"?username={search_str}")

        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(
                username__icontains=search_str
            ))
        )

    def test_search_driver_with_zero_results(self) -> None:
        search_str = "adwd"
        response = self.client.get(DRIVER_LIST_URL + f"?username={search_str}")

        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(
                username__icontains=search_str
            ))
        )

    def test_create_driver(self) -> None:
        form_data = {
            "username": "new_user",
            "password1": "test123test",
            "password2": "test123test",
            "license_number": "ABC12345",
            "first_name": "Test first",
            "last_name": "Test last",
        }
        response = self.client.post(DRIVER_CREATE_URL, data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(
            new_user.get_full_name(),
            (form_data["first_name"] + " " + form_data["last_name"])
        )
        self.assertEqual(new_user.license_number, form_data["license_number"])
        self.assertTrue(new_user.check_password(form_data["password1"]))

    def test_update_car_license_number_with_valid_data(self) -> None:
        form_data = {
            "license_number": "ABC12345"
        }
        response = self.client.post(DRIVER_UPDATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_update_car_license_number_with_no_valid_data(self) -> None:
        form_data = {
            "license_number": "ABC1234"
        }
        response = self.client.post(DRIVER_UPDATE_URL, data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_driver(self) -> None:
        response = self.client.post(DRIVER_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=ID).exists()
        )
