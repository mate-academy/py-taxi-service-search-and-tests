from django.contrib.auth import get_user_model
from django.forms import fields_for_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    SearchForm
)
from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")

CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")

PAGINATION = 5


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer", country="TestCountry"
        )

    def test_manufacturer_unauthorized_required_list(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_unauthorized_required_create(self) -> None:
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_unauthorized_required_update(self) -> None:
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.pk])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_unauthorized_required_delete(self) -> None:
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.pk])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        number_of_manufacturer = 14
        list_of_manufacturer = []
        for manufacturer in range(number_of_manufacturer):
            list_of_manufacturer.append(
                Manufacturer(
                    name=f"TestName{manufacturer}",
                    country=f"TestCountry{manufacturer}",
                )
            )
        Manufacturer.objects.bulk_create(list_of_manufacturer)

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUsername", password="TestPassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self) -> None:
        search_field = "name"
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()[:PAGINATION]
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            PAGINATION
        )
        self.assertEqual(response.context["search_field"], search_field)

    def test_retrieve_manufacturer_create(self) -> None:
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        expected_fields = list(fields_for_model(Manufacturer).keys())
        actual_fields = list(response.context.get("form").fields.keys())
        self.assertEqual(expected_fields, actual_fields)

        data = {"name": "CreateTest", "country": "CreateCountry"}
        url = reverse("taxi:manufacturer-create")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertTrue(
            Manufacturer.objects.filter(name="CreateTest").exists()
        )

    def test_retrieve_manufacturer_update(self) -> None:
        manufacturer = Manufacturer.objects.first()
        updated_data = {
            "name": "UpdatedTestName",
            "country": "UpdatedTestCountry"
        }
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": manufacturer.pk}
            ),
            data=updated_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertTemplateUsed(
            self.client.get(
                reverse("taxi:manufacturer-update",
                        kwargs={"pk": manufacturer.pk}
                        )
            ),
            "taxi/manufacturer_form.html",
        )

    def test_retrieve_manufacturer_delete_and_template(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="DeleteName", country="DeleteCountry"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.pk})
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        with self.assertRaises(manufacturer.DoesNotExist):
            Manufacturer.objects.get(pk=manufacturer.pk)


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        model = "X5 M"
        manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )

        driver = Driver.objects.create_user(
            username="TestUser",
            password="TestPassword",
            license_number="ABC12345"
        )

        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer,
        )

        self.car = Car.objects.create(
            model=model,
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)

    def test_car_unauthorized_required_list(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_unauthorized_required_create(self) -> None:
        response = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_unauthorized_required_detail(self) -> None:
        url = reverse("taxi:driver-detail", args=[self.car.pk])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_unauthorized_required_update(self) -> None:
        url = reverse("taxi:car-update", args=[self.car.pk])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_unauthorized_required_delete(self) -> None:
        url = reverse("taxi:car-delete", args=[self.car.pk])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer", country="TestCountry"
        )

        driver = Driver.objects.create_user(
            username="TestUser",
            password="TestPassword",
            license_number="ABC12345"
        )

        number_of_cars = 7
        for car_id in range(number_of_cars):
            car = Car.objects.create(
                model=f"TestModel{car_id}", manufacturer=manufacturer
            )
            car.drivers.add(driver)

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self) -> None:
        search_field_name = "model"
        with self.assertNumQueries(4):
            response = self.client.get(CAR_LIST_URL)
            self.assertEqual(response.status_code, 200)

        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["search_field"], search_field_name)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), PAGINATION)

    def test_form_class_create(self) -> None:
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertIsInstance(form, CarForm)

    def test_form_class_update(self) -> None:
        response = self.client.get(f"/cars/{Car.objects.first().pk}/update/")
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertIsInstance(form, CarForm)


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
            license_number="ABC12345"
        )

    def test_driver_unauthorized_required_list(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_unauthorized_required_create(self) -> None:
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_unauthorized_required_detail(self) -> None:
        url = reverse("taxi:driver-detail", args=[self.driver.pk])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_unauthorized_required_update(self) -> None:
        url = reverse("taxi:driver-update", args=[self.driver.pk])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_car_unauthorized_required_delete(self) -> None:
        url = reverse("taxi:driver-delete", args=[self.driver.pk])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        number_of_drivers = 7
        for driver_id in range(number_of_drivers):
            get_user_model().objects.create_user(
                username=f"TestUsername{driver_id}",
                password=f"TestPassword{driver_id}",
                license_number=f"ABC{driver_id}234",
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self) -> None:
        search_field_name = "username"
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["search_field"], search_field_name)

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), PAGINATION)

    def test_queryset_detail(self) -> None:
        driver = Driver.objects.first()
        response = self.client.get(f"/drivers/{driver.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], driver)

    def test_form_class_create(self) -> None:
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIsInstance(form, DriverCreationForm)

    def test_form_class_update(self) -> None:
        driver = Driver.objects.first()
        response = self.client.get(f"/drivers/{driver.pk}/update/")
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertIsInstance(form, DriverLicenseUpdateForm)


class SearchableListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        number_of_drivers = 5
        for driver_id in range(number_of_drivers):
            get_user_model().objects.create_user(
                username=f"TestDriver{driver_id}",
                password="TestPassword",
                license_number=f"ABC{driver_id}123",
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)

    def test_context_contains_search_field_and_form(self) -> None:
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["search_field"], "username")
        search_form = response.context["search_form"]
        self.assertIsInstance(search_form, SearchForm)
        self.assertEqual(search_form.initial["text"], "")

    def test_search_functionality(self) -> None:
        search_term = "TestDriver1"
        response = self.client.get(
            reverse("taxi:driver-list") + f"?text={search_term}"
        )
        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]
        self.assertEqual(len(driver_list), 1)
        self.assertEqual(driver_list[0].username, search_term)

    def test_empty_search_returns_all(self) -> None:
        response = self.client.get(reverse("taxi:driver-list") + "?text=")
        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]
        self.assertEqual(len(driver_list), 5)


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        number_of_drivers = 5
        for driver_id in range(number_of_drivers):
            Driver.objects.create_user(
                username=f"TestDriver{driver_id}",
                password="TestPassword",
                license_number=f"ABC{driver_id}123",
            )

        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer", country="TestCountry"
        )

        number_of_cars = 3
        for car_id in range(number_of_cars):
            Car.objects.create(
                model=f"TestModel{car_id}",
                manufacturer=manufacturer
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("taxi:index"))
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_context_data(self) -> None:
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["num_drivers"],
            Driver.objects.count()
        )
        self.assertEqual(response.context["num_cars"], Car.objects.count())
        self.assertEqual(
            response.context["num_manufacturers"], Manufacturer.objects.count()
        )

    def test_session_visits_increment(self) -> None:
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_visits"], 1)

        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 2)
