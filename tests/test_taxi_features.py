from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer
from django.db.utils import IntegrityError


class CoreFeaturesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="SecureUserP@ssw0rd!",
            first_name="Test",
            last_name="User",
            license_number="TST12345",
        )
        self.admin_user = get_user_model().objects.create_user(
            username="adminuser",
            password="SecureAdminP@ssw0rd!",
            is_staff=True,
            is_superuser=True,
            first_name="Admin",
            last_name="User",
            license_number="ADM98765",
        )
        self.client.login(username="adminuser", password="SecureAdminP@ssw0rd!")

        self.manufacturer1 = Manufacturer.objects.create(name="BMW", country="Germany")
        self.manufacturer2 = Manufacturer.objects.create(
            name="Mercedes", country="Germany"
        )
        self.car1 = Car.objects.create(model="X5", manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="C-Class", manufacturer=self.manufacturer2)
        self.driver1 = get_user_model().objects.create_user(
            username="driverone",
            password="SecureDriver1P@ssw0rd!",
            license_number="ABC11111",
            first_name="John",
            last_name="Doe",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="drivertwo",
            password="SecureDriver2P@ssw0rd!",
            license_number="XYZ22222",
            first_name="Jane",
            last_name="Smith",
        )
        self.driver_to_delete = get_user_model().objects.create_user(
            username="driver_del", password="delpass", license_number="DEL00000"
        )

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")

    def test_driver_list_view_authenticated(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertContains(response, "driverone")
        self.assertContains(response, "drivertwo")

    def test_create_manufacturer(self):
        initial_count = Manufacturer.objects.count()
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Audi", "country": "Germany"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Manufacturer.objects.count(), initial_count + 1)
        self.assertTrue(Manufacturer.objects.filter(name="Audi").exists())
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_driver_with_valid_data(self):
        initial_driver_count = Driver.objects.count()
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "newdriver",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
                "license_number": "LMN33333",
                "first_name": "New",
                "last_name": "Driver",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Driver.objects.count(), initial_driver_count + 1)
        new_driver = Driver.objects.get(username="newdriver")
        self.assertEqual(new_driver.license_number, "LMN33333")
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_create_driver_with_invalid_license_number(self):
        initial_driver_count = Driver.objects.count()
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "invalidlicense",
                "password1": "VeryStrongPassword123!@#",
                "password2": "VeryStrongPassword123!@#",
                "license_number": "invalid",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        self.assertEqual(
            response.status_code, 200
        )
        self.assertEqual(
            Driver.objects.count(), initial_driver_count
        )
        self.assertContains(
            response,
            "License number must consist of "
            "3 uppercase letters followed by 5 digits.",
        )

    def test_create_driver_duplicate_license_number(self):
        initial_driver_count = Driver.objects.count()
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "duplicatelicense",
                "password1": "AnotherStrongPassword!",
                "password2": "AnotherStrongPassword!",
                "license_number": "ABC11111",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        self.assertEqual(
            response.status_code, 200
        )
        self.assertEqual(
            Driver.objects.count(), initial_driver_count
        )
        self.assertContains(
            response, "A driver&#x27;s license with this number already exists."
        )

    def test_update_driver_license_number_with_valid_data(self):
        new_license = "UPT99999"
        response = self.client.post(
            reverse("taxi:driver-license-update", kwargs={"pk": self.driver1.id}),
            data={"license_number": new_license},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.driver1.refresh_from_db()
        self.assertEqual(self.driver1.license_number, new_license)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertContains(
            response, new_license
        )

    def test_update_driver_license_number_with_invalid_data(self):
        original_license = self.driver1.license_number
        invalid_license = "BAD"
        response = self.client.post(
            reverse("taxi:driver-license-update", kwargs={"pk": self.driver1.id}),
            data={"license_number": invalid_license},
        )
        self.assertEqual(response.status_code, 200)
        self.driver1.refresh_from_db()
        self.assertEqual(
            self.driver1.license_number, original_license
        )
        self.assertContains(
            response,
            "The license number must consist of "
            "3 capital letters and 5 digits.",
        )

    def test_delete_driver(self):
        initial_driver_count = Driver.objects.count()
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": self.driver_to_delete.id}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Driver.objects.count(), initial_driver_count - 1)
        self.assertFalse(Driver.objects.filter(id=self.driver_to_delete.id).exists())
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class SearchFeatureTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="SecureSearchP@ssw0rd!"
        )
        self.client.login(username="testuser", password="SecureSearchP@ssw0rd!")

        self.driver_john = get_user_model().objects.create_user(
            username="john_doe", password="SecureJohnP@ssw0rd!", license_number="JHN12345"
        )
        self.driver_jane = get_user_model().objects.create_user(
            username="jane_smith", password="SecureJaneP@ssw0rd!", license_number="JNE67890"
        )
        self.manufacturer_bmw = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.manufacturer_audi = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        self.manufacturer_honda = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )

        self.car_bmw_x5 = Car.objects.create(
            model="X5", manufacturer=self.manufacturer_bmw
        )
        self.car_bmw_x3 = Car.objects.create(
            model="X3", manufacturer=self.manufacturer_bmw
        )
        self.car_audi_a4 = Car.objects.create(
            model="A4", manufacturer=self.manufacturer_audi
        )

    def test_driver_search_by_username(self):
        response = self.client.get(reverse("taxi:driver-list"), {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")

    def test_driver_search_by_username_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "nonexistent"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")
        self.assertContains(response, "There are no drivers in the service.")

    def test_driver_search_case_insensitive(self):
        response = self.client.get(reverse("taxi:driver-list"), {"username": "JOhN"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")

    def test_car_search_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "X"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")
        self.assertContains(response, "X3")
        self.assertNotContains(response, "A4")

    def test_car_search_by_model_full_match(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "A4"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A4")
        self.assertNotContains(response, "X5")

    def test_car_search_no_results(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "Z1"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "X5")
        self.assertContains(response, "There are no cars in taxi")

    def test_manufacturer_search_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "BMW"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")

    def test_manufacturer_search_partial_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "au"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audi")
        self.assertNotContains(response, "BMW")

    def test_manufacturer_search_no_results(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "Volvo"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "BMW")
        self.assertContains(response, "There are no manufacturers in the service.")
