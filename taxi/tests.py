from django.test import TestCase, Client

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    CarSearchForm
)

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class TestForm(TestCase):
    def test_driver_with_license_number_is_valid(self):
        data = {
            "username": "test",
            "password1": "A$test1234",
            "password2": "A$test1234",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "license_number": "AAA12345",
        }

        form = DriverCreationForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, data)

    def test_driver_with_invalid_license_number(self):
        data = {
            "username": "test",
            "password1": "A$test1234",
            "password2": "A$test1234",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "license_number": "aaa12345",
        }

        form = DriverCreationForm(data=data)

        self.assertFalse(form.is_valid())

    def test_driver_search_form_label_field(self):
        form = DriverSearchForm()
        self.assertEquals(form.fields["username"].label, "")

    def test_driver_search_form_required_field(self):
        form = DriverSearchForm()
        self.assertTrue(form.fields["username"].required)

    def test_manufacturer_search_form_max_length(self):
        form = ManufacturerSearchForm()
        self.assertEquals(form.fields["name"].max_length, 255)

    def test_car_search_form_widget_placeholder_exist(self):
        form = CarSearchForm()
        widget = form.fields["model"].widget
        self.assertTrue(
            widget.__dict__["attrs"]["placeholder"]
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateDriverTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_drivers = 10
        for driver_id in range(number_of_drivers):
            Driver.objects.create(
                first_name=f"test {driver_id}",
                last_name=f"surname {driver_id}",
                license_number=f"TTT1{(driver_id+1) % 10}34{driver_id % 10}",
                username=f"username {driver_id}",
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )

        self.client.force_login(self.user)

    def test_url_all_drivers_exist(self):
        response = self.client.get("/drivers/")
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEquals(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_pagination_is_2(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEquals(len(response.context["driver_list"]), 2)

    def test_page_6_with_one_driver(self):
        response = self.client.get(reverse("taxi:driver-list") + "?page=6")
        self.assertEquals(len(response.context["driver_list"]), 1)

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "A$test1234",
            "password2": "A$test1234",
            "license_number": "AAA12345",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = Driver.objects.get(username=form_data["username"])

        self.assertEquals(new_driver.username, form_data["username"])
        self.assertEquals(new_driver.last_name, form_data["last_name"])
        self.assertEquals(
            new_driver.license_number,
            form_data["license_number"]
        )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )

        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="country1"
        )
        Car.objects.create(model="Opel", manufacturer=manufacturer)
        Car.objects.create(model="Nissan", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEquals(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEquals(list(response.context["car_list"]), list(cars))


class CarSearchModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="country1"
        )
        models = [
            "nissan",
            "opel",
            "volskvagen",
            "mercedes",
            "kia",
            "shevrolet",
            "renault"
        ]
        for model in models:
            Car.objects.create(model=model, manufacturer=manufacturer)

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )

        self.client.force_login(self.user)

    def test_search_model_car_with_single_letter(self):
        char = "a"
        response = self.client.get(f"/cars/?model={char}")
        car_with_letter_a = Car.objects.filter(model__icontains=char)
        self.assertEquals(
            list(response.context["car_list"]),
            list(car_with_letter_a)[:3]
        )

    def test_search_model_car_with_uppercase_letters(self):
        char = "AN"
        response = self.client.get(f"/cars/?model={char}")
        car_with_letter_a = Car.objects.filter(model__icontains=char)
        self.assertEquals(
            list(response.context["car_list"]),
            list(car_with_letter_a)[:3]
        )

    def test_search_model_car_page_2(self):
        char = "A"
        response = self.client.get(f"/cars/?model={char}&page=2")
        car_with_letter_a = Car.objects.filter(model__icontains=char)
        self.assertEquals(
            list(response.context["car_list"]),
            list(car_with_letter_a)[3:6]
        )

    def test_search_model_car_by_exact_name(self):
        response = self.client.get("/cars/?model=opel")
        opel = Car.objects.filter(model="opel")
        self.assertEquals(list(response.context["car_list"]), list(opel))


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Opel",
            country="Germany"
        )
        self.assertEquals(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="michael",
            first_name="Michael",
            last_name="Schumacher",
            password="test1234",
        )

        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_with_license_number(self):
        username = "michael"
        first_name = "Michael"
        last_name = "Schumacher"
        password = "test1234"
        license_number = "LICENSE"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            license_number=license_number,
        )

        self.assertEquals(driver.username, username)
        self.assertEquals(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Opel",
            country="Germany"
        )
        car = Car.objects.create(model="audi", manufacturer=manufacturer)

        self.assertEquals(str(car), car.model)

    def test_manufacturer_ordering(self):
        manufacturer1 = Manufacturer.objects.create(
            name="opel",
            country="country1"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="alfa romeo", country="country2"
        )
        manufacturer3 = Manufacturer.objects.create(
            name="nissan",
            country="country3"
        )
        manufacturer4 = Manufacturer.objects.create(
            name="citroen",
            country="country4"
        )

        all_manufacturers = list(Manufacturer.objects.all())

        self.assertEquals(
            all_manufacturers,
            [manufacturer2, manufacturer4, manufacturer3, manufacturer1],
        )

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create(
            username="michael",
            first_name="Michael",
            last_name="Schumacher",
            password="test1234",
        )
        self.assertEquals(driver.get_absolute_url(), f"/drivers/{driver.id}/")

    def test_driver_license_number_max_length(self):
        driver = get_user_model().objects.create(
            username="michael",
            first_name="Michael",
            last_name="Schumacher",
            password="test1234",
        )
        self.assertEquals(
            driver._meta.get_field("license_number").max_length, 255
        )

    def test_car_blank_false(self):
        car = Car.objects.create(
            model="Opel",
            manufacturer=Manufacturer.objects.create(
                name="test",
                country="country1"
            ),
        )
        self.assertFalse(car._meta.get_field("model").blank)


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test", password="test1234"
        )

        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test1234",
            license_number="LICENSE"
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)
