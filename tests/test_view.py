from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Driver, Car, Manufacturer


class PublicViewTests(TestCase):
    def setUp(self):
        self.index_url = reverse("taxi:index")
        self.manufacturer_list_url = reverse("taxi:manufacturer-list")
        self.manufacturer_create_url = reverse("taxi:manufacturer-create")
        self.car_list_url = reverse("taxi:car-list")
        self.driver_list_url = reverse("taxi:driver-list")
        self.driver_create_url = reverse("taxi:driver-create")

    def test_login_required(self):
        urls = [self.index_url,
                self.manufacturer_list_url,
                self.manufacturer_create_url,
                self.car_list_url,
                self.driver_list_url,
                self.driver_create_url]

        for url in urls:
            response = self.client.get(url)
            self.assertNotEquals(response.status_code, 200)


class IndexViewTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test_driver",
            password="PASSWORD",
            license_number="TST1221"
        )
        self.index_url = reverse("taxi:index")
        self.user = Driver.objects.create_user(
            username="test",
            password="password")
        self.client.force_login(self.user)
        self.response = self.client.get(self.index_url)

    def test_correctness_template(self):
        self.assertTemplateUsed(self.response, "taxi/index.html")

    def test_driver_counter_presents(self):
        num_drivers = Driver.objects.count()
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(
            self.response.context["num_drivers"],
            num_drivers,
        )

    def test_driver_car_counter_presents(self):
        num_cars = Car.objects.count()
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context["num_cars"], num_cars)

    def test_driver_manufacturer_counter_presents(self):
        num_manufacturers = Manufacturer.objects.count()
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context["num_cars"], num_manufacturers)

    def test_driver_numvisits_counter_presents(self):
        self.assertEqual(self.response.context["num_visits"], 1)
        self.response = self.client.get(self.index_url)
        self.assertEqual(self.response.context["num_visits"], 2)


class ManufacturerViewTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.manufacturer_url = reverse("taxi:manufacturer-list")
        self.user = Driver.objects.create_user(
            username="test",
            password="password")
        self.client.force_login(self.user)
        self.response = self.client.get(self.manufacturer_url)

    def test_correctness_template(self):
        self.assertTemplateUsed(self.response, "taxi/manufacturer_list.html")

    def test_search_fields_present(self):
        form = ManufacturerSearchForm(data={"name": "test"})
        form.is_valid()
        self.assertEqual(form.cleaned_data, form.data)

    def test_get_queryset(self):
        request = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "test_name"}
        )
        self.assertContains(request, self.manufacturer.name)


class CarViewTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.driver = Driver.objects.create_user(
            username="test",
            password="PASSWORD",
            license_number="ASD1221"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)
        self.client.force_login(self.driver)
        self.car_list = reverse("taxi:car-list")
        self.response = self.client.get(self.car_list)

    def test_car_search_present(self):
        form = CarSearchForm(data={"model": "test_model"})
        form.is_valid()
        self.assertEqual(form.cleaned_data, form.data)

    def test_get_queryset(self):
        request = self.client.get(
            reverse("taxi:car-list"), {"model": "test_model"}
        )
        self.assertContains(request, self.car.model)


class DriverViewTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test",
            password="PASSWORD",
            license_number="ASD1221"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.client.force_login(self.driver)
        self.car_list = reverse("taxi:car-list")
        self.response = self.client.get(self.car_list)

    def test_driver_search_present(self):
        form = DriverSearchForm(data={"username": "test"})
        form.is_valid()
        self.assertEqual(form.cleaned_data, form.data)

    def test_get_queryset(self):
        request = self.client.get(
            reverse("taxi:driver-list"), {"username": "test"}
        )
        self.assertContains(request, self.driver.username)

    def test_assign_unassign_driver_to_car(self):
        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.pk]))
        self.car.drivers.filter(pk=self.driver.pk).exists()
        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.pk]))
        self.car.drivers.filter(pk=self.driver.pk).exists()
        self.assertNotIn(self.driver, self.car.drivers.all())
