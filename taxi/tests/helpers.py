from taxi.models import Manufacturer, Car
from django.contrib.auth import get_user_model


def create_test_data():
    manufacturer = Manufacturer.objects.create(
        name="Test manufacturer",
        country="Test country"
    )
    driver = get_user_model().objects.create(
        username="test_driver",
        password="test_password123",
        first_name="test first",
        last_name="test last",
        license_number="ABC12345",
    )
    car = Car.objects.create(
        model="Test model",
        manufacturer=manufacturer,
    )
    car.drivers.add(driver)
    return manufacturer, driver, car
