from django.test import TestCase

from taxi.models import Driver
from django.urls import reverse


class PublicViewTest(TestCase):

    def test_login_required(self):
        resp_driver_list = self.client.get(reverse("taxi:driver-list"))
        resp_car_list = self.client.get(reverse("taxi:car-list"))
        resp_manufacturer_list = self.client.get(reverse("taxi:manufacturer-list"))
        resp_login = self.client.get(reverse("login"))
        resp_index = self.client.get(reverse("taxi:index"))

        self.assertEqual(resp_driver_list.status_code, 302)
        self.assertEqual(resp_car_list.status_code, 302)
        self.assertEqual(resp_manufacturer_list.status_code, 302)
        self.assertEqual(resp_index.status_code, 302)
        self.assertEqual(resp_login.status_code, 200)


# class PrivateViewTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         number_of_drivers = 15
#         for driver_num in range(number_of_drivers):
#             Driver.objects.create_user(username="chris %s" % driver_num,
#                                        password="chris %s" % driver_num,
#                                        first_name="Christian %s" % driver_num,
#                                        last_name="Surname %s" % driver_num,
#                                        license_number=f"BHJ1234{driver_num}")


