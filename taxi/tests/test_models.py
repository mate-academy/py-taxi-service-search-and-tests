from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverModelTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="dirvertest",
            first_name="First",
            last_name="Lasts",
            license_number="CAD25252",
            password="drivepass22",
        )

        self.client.force_login(self.user)

    def test_driver_created(self) -> None:
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            get_user_model().objects.filter(id=self.user.id).exists()
        )

    def test_driver_deleted(self) -> None:
        new_driver = get_user_model().objects.create(
            username="random.test",
            license_number="TTT11112",
            first_name="Temp",
            last_name="Temps",
            password="222asdfg",
        )

        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": new_driver.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=new_driver.id).exists()
        )
