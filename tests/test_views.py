from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test", "password123"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Lanos")
        Manufacturer.objects.create(name="Lamborghini")
        Manufacturer.objects.create(name="Laptop")
        Manufacturer.objects.create(name="Toyota")

    def test_manufacturer_retrieve(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search_form_with_name(self):
        response = self.client.get(MANUFACTURER_URL, {
            "name": "toyo"
        })
        manufacturers = Manufacturer.objects.all()
        queryset = manufacturers.filter(name__icontains="toyo")
        self.assertEqual(list(
            response.context["manufacturer_list"]), list(queryset)
        )

    def test_manufacturer_search_form_with_name_which_doesnt_exist(self):
        response = self.client.get(MANUFACTURER_URL, {
            "name": "Mer"
        })
        manufacturers = Manufacturer.objects.all()
        queryset = manufacturers.filter(name__icontains="Mer")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(queryset)
        )

    def test_manufacturer_search_form_with_simular_names(self):
        response = self.client.get(MANUFACTURER_URL, {
            "name": "La"
        })
        manufacturers = Manufacturer.objects.all()
        queryset = manufacturers.filter(name__icontains="La")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(queryset)
        )


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test", "password123"
        )
        self.client.force_login(self.user)
        Driver.objects.create(username="user_busy", license_number="ABC12645")
        Driver.objects.create(username="test_driv", license_number="ASC12354")
        Driver.objects.create(username="best_driv", license_number="ACH09876")

    def test_create_driver(self):
        form_data = {
            "username": "new_driver",
            "password1": "user123test",
            "password2": "user123test",
            "license_number": "ABC12345",
            "first_name": "User",
            "last_name": "Shift",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_driver_search_form_with_username(self):
        response = self.client.get(DRIVER_URL, {
            "username": "busy"
        })
        drivers = Driver.objects.all()
        queryset = drivers.filter(username__icontains="busy")
        self.assertEqual(list(response.context["driver_list"]), list(queryset))

    def test_driver_search_form_with_username_which_doesnt_exist(self):
        response = self.client.get(DRIVER_URL, {
            "username": "kerovca"
        })
        drivers = Driver.objects.all()
        queryset = drivers.filter(username__icontains="kerovca")
        self.assertEqual(list(response.context["driver_list"]), list(queryset))

    def test_driver_search_form_with_simular_usernames(self):
        response = self.client.get(DRIVER_URL, {
            "username": "driv"
        })
        drivers = Driver.objects.all()
        queryset = drivers.filter(username__icontains="driv")
        self.assertEqual(list(response.context["driver_list"]), list(queryset))


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test", "password123"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(model="work_car", manufacturer=manufacturer)
        Car.objects.create(model="business_car", manufacturer=manufacturer)
        Car.objects.create(model="best_machine", manufacturer=manufacturer)

    def test_car_search_form_with_model(self):
        response = self.client.get(CAR_URL, {"model": "wo"})
        cars = Car.objects.all()
        queryset = cars.filter(model__icontains="wo")
        self.assertEqual(list(response.context["car_list"]), list(queryset))

    def test_car_search_form_with_model_which_doesnt_exist(self):
        response = self.client.get(CAR_URL, {"model": "tachka"})
        cars = Car.objects.all()
        queryset = cars.filter(model__icontains="tachka")
        self.assertEqual(list(response.context["car_list"]), list(queryset))

    def test_car_search_form_with_simular_models(self):
        response = self.client.get(CAR_URL, {
            "model": "car"
        })
        cars = Car.objects.all()
        queryset = cars.filter(model__icontains="car")
        self.assertEqual(list(response.context["car_list"]), list(queryset))
