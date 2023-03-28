from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AnonymousPermDenied(TestCase):
    """The same tests should be implemented for all the other views"""

    def setUp(self):
        self.client = Client()

    def test_homepage_anon_denied(self):
        address = reverse("taxi:index")
        request = self.client.get(address)
        self.assertNotEqual(request.status_code, "200")


class AssignCarWorkCorrect(TestCase):
    """The same tests should be implemented
    for other update and create views"""

    def setUp(self):
        self.client = Client()
        get_user_model().objects.create_user(
            username="little_ann",
            password="12345",
            license_number="AAA12345",
        )
        manufacturer = Manufacturer.objects.create(
            name="Mazda", country="Germany"
        )
        Car.objects.create(
            model="Gimlet", manufacturer=manufacturer
        )

    def test_redirect_after_change_drivers_car_list(self):
        car = Car.objects.get(model="Gimlet")
        user = get_user_model().objects.get(username="little_ann")
        self.client.force_login(user)
        address = reverse("taxi:toggle-car-assign", args=[car.id])
        destination = reverse("taxi:car-detail", args=[car.id])
        request = self.client.get(address)
        self.assertRedirects(request, destination)

    def test_car_was_assigned(self):
        car = Car.objects.get(model="Gimlet")
        user = get_user_model().objects.get(username="little_ann")
        self.client.force_login(user)
        address = reverse("taxi:toggle-car-assign", args=[car.id])
        self.client.get(address)
        self.assertTrue(car in user.cars.all())


class RetrieveCorrectData(TestCase):
    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Mazda", country="Germany"
        )
        Manufacturer.objects.create(
            name="Suzuki", country="Japan"
        )
        user = get_user_model().objects.create_user(
            username="little_ann",
            password="12345",
            license_number="AAA12345",
        )
        self.client.force_login(user)
        address = reverse("taxi:manufacturer-list")
        response = self.client.get(address)
        manufacturers = Manufacturer.objects.all()
        self.assertTrue(
            list(manufacturers),
            list(response.context["manufacturer_list"])
        )


class ChangeData(TestCase):
    def test_license_number_changed(self):
        self.client = Client()
        user = get_user_model().objects.create_user(
            username="little_ann",
            password="12345",
            license_number="AAA12345",
        )
        self.client.force_login(user)
        address = reverse("taxi:driver-update", args=[user.id])
        self.client.post(address, {"license_number": "QQQ99999"})
        user.refresh_from_db()
        self.assertEqual(user.license_number, "QQQ99999")


class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        manufacturer = Manufacturer.objects.create(
            name="Mazda", country="Germany"
        )
        Manufacturer.objects.create(
            name="Kamaz", country="Ukraine"
        )
        Manufacturer.objects.create(
            name="Suzuki", country="Japan"
        )
        Car.objects.create(
            model="Gimlet", manufacturer=manufacturer
        )
        Car.objects.create(
            model="Vitara", manufacturer=manufacturer
        )
        Car.objects.create(
            model="Yara", manufacturer=manufacturer
        )
        get_user_model().objects.create_user(
            username="little_ann",
            password="12345",
            license_number="AAA12345",
        )
        get_user_model().objects.create_user(
            username="Liberty",
            password="12445",
            license_number="AAA89345",
        )
        get_user_model().objects.create_user(
            username="antonio",
            password="12222345",
            license_number="AAA00345",
        )
        user = get_user_model().objects.get(username="little_ann")
        self.client.force_login(user)

    def test_driver_search(self):
        address = reverse("taxi:driver-list")
        response = self.client.get(address, data={"search_text": "An"})
        drivers = get_user_model().objects.filter(username__icontains="An")
        self.assertEqual(list(drivers), list(response.context["driver_list"]))

    def test_car_search(self):
        address = reverse("taxi:car-list")
        response = self.client.get(address, data={"search_text": "ra"})
        cars = Car.objects.filter(model__icontains="Ra")
        self.assertEqual(list(cars), list(response.context["car_list"]))

    def test_manufacturer_search(self):
        address = reverse("taxi:manufacturer-list")
        response = self.client.get(address, data={"search_text": "aZ"})
        cars = Manufacturer.objects.filter(name__icontains="aZ")
        self.assertEqual(
            list(cars),
            list(response.context["manufacturer_list"])
        )
