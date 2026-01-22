from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})
CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
CAR_UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": 1})
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_DELETE_URL = reverse("taxi:car-delete", kwargs={"pk": 1})
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_UPDATE_URL = reverse("taxi:driver-update", kwargs={"pk": 1})
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_DELETE_URL = reverse("taxi:driver-delete", kwargs={"pk": 2})


class PublicTest(TestCase):

    def setUp(self):
        self.client = Client()
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )
        manufacturer.save()
        Car.objects.create(
            model="Test Car",
            manufacturer=manufacturer,
        )
        Driver.objects.create_user(
            username="Test Driver",
            password="<PASSWORD>",
            first_name="Test First",
            last_name="Test Last",
            license_number="AAA11111",
        )
        self.urls = [
            MANUFACTURER_LIST_URL,
            MANUFACTURER_UPDATE_URL,
            MANUFACTURER_CREATE_URL,
            MANUFACTURER_DELETE_URL,
            CAR_LIST_URL,
            CAR_DETAIL_URL,
            CAR_UPDATE_URL,
            CAR_CREATE_URL,
            CAR_DELETE_URL,
            DRIVER_LIST_URL,
            DRIVER_DETAIL_URL,
            DRIVER_UPDATE_URL,
            DRIVER_CREATE_URL,
            DRIVER_DELETE_URL,
        ]

    def test_login_required(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="Test Driver",
            password="<PASSWORD>",
            first_name="Test First",
            last_name="Test Last",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_objects(self):
        Manufacturer.objects.create(name="Test 1", country="US")
        Manufacturer.objects.create(name="Test 2", country="US")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_get_context_data(self):
        Manufacturer.objects.create(name="Test 1", country="US")
        Manufacturer.objects.create(name="Test 2", country="US")
        response = self.client.get(MANUFACTURER_LIST_URL)
        context = response.context
        search_form = ManufacturerSearchForm(
            initial={"name": ""}
        )
        self.assertEqual(
            str(context["search_form"]),
            str(search_form)
        )

    def test_get_queryset(self):
        Manufacturer.objects.create(name="Test 1", country="US")
        Manufacturer.objects.create(name="Test 2", country="US")
        response = self.client.get(MANUFACTURER_LIST_URL, data={"name": "1"})
        manufacturers = Manufacturer.objects.filter(name__icontains="1")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_manufacturer_create_view(self):
        form_data = {"name": "Test Manufacturer", "country": "US", }
        response = self.client.post(MANUFACTURER_CREATE_URL, form_data,)
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        manufacturer = Manufacturer.objects.get(name="Test Manufacturer")
        self.assertEqual(manufacturer.country, "US")

    def test_manufacturer_update_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US"
        )
        form_data = {"name": "Manufacturer 1", "country": "USA", }
        response = self.client.post(reverse(
            "taxi:manufacturer-update", kwargs={"pk": manufacturer.id}),
            form_data,
        )
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, form_data["name"])
        self.assertEqual(manufacturer.country, form_data["country"])

    def test_manufacturer_delete_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="USA"
        )
        Manufacturer.objects.create(name="Test Manufacturer 2", country="USA")
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": manufacturer.id}
            ),
            follow=True
        )
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )


class PrivateCarTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test 1",
            country="US"
        )
        self.user = Driver.objects.create_user(
            username="Test Driver",
            password="<PASSWORD>",
            first_name="Test First",
            last_name="Test Last",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)

    def test_retrieve_car_objects(self):
        Car.objects.create(model="Test car 1", manufacturer=self.manufacturer)
        Car.objects.create(model="Test car 2", manufacturer=self.manufacturer)
        Car.objects.create(model="Test car 3", manufacturer=self.manufacturer)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        Car.objects.create(model="Test car 4", manufacturer=self.manufacturer)
        Car.objects.create(model="Test car 5", manufacturer=self.manufacturer)
        Car.objects.create(model="Test car 6", manufacturer=self.manufacturer)
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()[:5]
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_get_context_data(self):
        Car.objects.create(model="Test car 1", manufacturer=self.manufacturer)
        Car.objects.create(model="Test car 2", manufacturer=self.manufacturer)
        response = self.client.get(CAR_LIST_URL)
        context = response.context
        search_form = CarSearchForm(
            initial={"model": ""}
        )
        self.assertEqual(
            str(context["search_form"]),
            str(search_form)
        )

    def test_get_queryset(self):
        Car.objects.create(model="Test car 1", manufacturer=self.manufacturer)
        Car.objects.create(model="Test car 2", manufacturer=self.manufacturer)
        response = self.client.get(CAR_LIST_URL, data={"model": "1"})
        cars = Car.objects.filter(model__icontains="1")[:5]
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_car_create_view(self):
        form_data = {
            "model": "Test car 1",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        }
        response = self.client.post(reverse("taxi:car-create"), form_data,)
        self.assertRedirects(response, CAR_LIST_URL)
        car = Car.objects.get(id=self.user.cars.first().id)
        self.assertEqual(car.model, "Test car 1")
        self.assertEqual(car.manufacturer.id, form_data["manufacturer"])

    def test_car_update_view(self):
        car = Car.objects.create(
            model="Test 1",
            manufacturer=self.manufacturer
        )
        form_data = {
            "model": "Test car 1",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        response = self.client.post(
            reverse(
                "taxi:car-update",
                kwargs={"pk": car.id}
            ),
            form_data,
        )
        self.assertRedirects(response, CAR_LIST_URL)
        car.refresh_from_db()
        self.assertEqual(car.model, form_data["model"])
        self.assertEqual(car.drivers.first().id, form_data["drivers"][0])

    def test_car_delete_view(self):
        car = Car.objects.create(
            model="Test 1",
            manufacturer=self.manufacturer
        )
        response = self.client.get(
            reverse(
                "taxi:car-delete",
                kwargs={"pk": car.id}
            )
        )
        self.assertContains(response, "Delete car?")
        response = self.client.post(
            reverse(
                "taxi:car-delete",
                kwargs={"pk": car.id}
            ),
            follow=True
        )
        self.assertRedirects(response, CAR_LIST_URL)
        cars = Car.objects.all()
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertEqual(len(list(cars)), 0)

    def test_car_detail_view(self):
        car = Car.objects.create(
            model="Test 1",
            manufacturer=self.manufacturer
        )
        response = self.client.get(
            reverse(
                "taxi:car-detail",
                kwargs={"pk": car.id}
            )
        )
        self.assertContains(response, "Delete")
        self.assertContains(response, "Update")
        self.assertContains(response, "Assign me from this car")
        self.assertContains(response, "Manufacturer:")
        self.assertContains(response, "Drivers")

    def test_toggle_assign_to_car(self):
        car = Car.objects.create(
            model="Test 1",
            manufacturer=self.manufacturer
        )
        response = self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": car.id}
            )
        )
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", kwargs={"pk": car.id})
        )
        self.assertEqual(self.user.cars.first(), car)
        response = self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": car.id}
            )
        )
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", kwargs={"pk": car.id})
        )
        self.assertEqual(len(list(self.user.cars.all())), 0)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="Test Driver",
            password="<PASSWORD>",
            first_name="Test First",
            last_name="Test Last",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_objects(self):
        for i in range(5):
            Driver.objects.create_user(
                username=f"Test {i+1}",
                password="<PASSWORD>",
                first_name="Test First",
                last_name="Test Last",
                license_number=f"AAA1111{i+2}",
            )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()[:5]
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_get_context_data(self):
        response = self.client.get(DRIVER_LIST_URL)
        search_form = DriverSearchForm(
            initial={"username": ""}
        )
        self.assertEqual(
            str(response.context["search_form"]),
            str(search_form)
        )

    def test_get_queryset(self):
        Driver.objects.create_user(
            username="Test 1",
            password="<PASSWORD>",
            first_name="New",
            last_name="Driver",
            license_number="AAA11112",
        )
        response = self.client.get(DRIVER_LIST_URL, data={"username": " 1"})
        drivers = Driver.objects.filter(username__icontains=" 1")[:5]
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_delete_driver(self):
        Driver.objects.create_user(
            username="Test 1",
            password="<PASSWORD>",
            first_name="Test First",
            last_name="Test Last",
            license_number="AAA11112",
        )
        response = self.client.get(DRIVER_DELETE_URL)
        self.assertContains(response, "Delete driver?")
        response = self.client.post(DRIVER_DELETE_URL, follow=True)
        self.assertRedirects(response, DRIVER_LIST_URL, status_code=302)

    def test_update_driver_license_number(self):
        form_data = {"license_number": "AAA11113", }
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data=form_data
        )
        self.assertRedirects(response, DRIVER_LIST_URL, status_code=302)

    def test_update_driver_license_number_with_not_valid_number(self):
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": "AAA1111", }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "License number should consist of 8 characters"
        )
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": "aaa11111", }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "First 3 characters should be uppercase letters"
        )
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": "AA111111", }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "First 3 characters should be uppercase letters"
        )
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": "AAAa1111", }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Last 5 characters should be digits")

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse(
                "taxi:driver-detail",
                kwargs={"pk": self.user.id}
            )
        )
        self.assertContains(response, "Delete")
        self.assertContains(response, "Update license number")
        self.assertContains(response, "First name:")
        self.assertContains(response, "Last name:")
        self.assertContains(response, "License number:")
        self.assertContains(response, "Is staff:")
        self.assertContains(response, "Cars")
