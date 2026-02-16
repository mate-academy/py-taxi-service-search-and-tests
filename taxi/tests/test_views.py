from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicTaxiTest(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaxiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",)
        self.client.force_login(self.user)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test123",
            first_name="Test First",
            last_name="Test Last",
            license_number="JOD26458",)

        self.manufacturer = Manufacturer.objects.create(
            name="Test Company",
            country="Test Country",)

        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer,)
        self.car.drivers.add(self.driver)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers))

    def test_retrieve_car(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars))

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers))

    def test_create_user(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "JOG26458",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PrivateTaxiSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",)
        self.client.force_login(self.user)

    def test_search_manufacturers_by_name(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Mitsubishi",
            country="Japan",
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Mazda",
            country="Japan",
        )
        manufacturer3 = Manufacturer.objects.create(
            name="Renault",
            country="France",
        )

        filter_names = ["M", "A","Renau", "Mazda"]

        for filter_name in filter_names:
            manufacturers_query = MANUFACTURER_URL + f"?name={filter_name}"
            response = self.client.get(manufacturers_query)
            filtered_manufacturers = Manufacturer.objects.filter(name__icontains=filter_name)
            self.assertEqual(
                list(response.context["paginator"].object_list),
                list(filtered_manufacturers),
            )

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan",
        )
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test123",
            license_number="JOD26458",
        )

        car1 = Car.objects.create(
            model="Mitsubishi Lancer",
            manufacturer=manufacturer,
        )
        car1.drivers.add(self.driver)

        car2 = Car.objects.create(
            model="Mitsubishi Eclipse",
            manufacturer=manufacturer,
        )
        car2.drivers.add(self.driver)

        car3 = Car.objects.create(
            model="Suzuki Vipara",
            manufacturer=manufacturer,
        )
        car3.drivers.add(self.driver)

        filter_models = ["e", "p", "Mit", "Lancer"]

        for filter_model in filter_models:
            models_query = CAR_URL + f"?model={filter_model}"
            response = self.client.get(models_query)
            filtered_models = Car.objects.filter(model__icontains=filter_model)
            self.assertEqual(
                list(response.context["paginator"].object_list),
                list(filtered_models),
            )

    def test_search_driver_by_username(self):
        driver1 = get_user_model().objects.create_user(
            username = "joyce.byers",
            password = "test123",
            license_number = "KOY26458",
        )
        driver2 = get_user_model().objects.create_user(
            username = "jonader.byers",
            password = "test123",
            license_number = "KOD26458",
        )
        driver2 = get_user_model().objects.create_user(
            username = "dustin.henderson",
            password = "test123",
            license_number = "KOK26458",
        )

        filter_usernames = ["j", "byers", "der"]

        for filter_username in filter_usernames:
            usernames_query = DRIVER_URL + f"?username={filter_username}"
            response = self.client.get(usernames_query)
            filtered_usernames = get_user_model().objects.filter(
                username__icontains=filter_username
            )
            self.assertEqual(
                list(response.context["paginator"].object_list),
                list(filtered_usernames),
            )
