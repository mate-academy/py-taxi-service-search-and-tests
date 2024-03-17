from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateDriverViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            email="<EMAIL>",
            password="<PASSWORD>")
        self.client.force_login(self.user)

    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_logout(self):
        self.client.logout()
        response = self.client.get(DRIVER_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_update_driver_view(self):
        joe = get_user_model().objects.create(
            first_name="Joe",
            license_number="WER67890"
        )
        joe.first_name = "Jack"
        joe.save()

        update_joe = get_user_model().objects.get(pk=joe.id)
        self.assertEqual(update_joe.first_name, "Jack")

    def test_delete_driver_view(self):
        diana = get_user_model().objects.create(
            first_name="Diana",
            license_number="WER67896"
        )
        self.assertEqual(get_user_model().objects.count(), 2)
        diana.delete()
        self.assertEqual(get_user_model().objects.count(), 1)
