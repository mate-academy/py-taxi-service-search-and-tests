import itertools
from typing import Iterator

from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car
import random

SEEDS = [42, 47, 13]
CARS_AMOUNT = 12
MANUFACTURERS_AMOUNT = 8
DRIVERS_AMOUNT = 12

custom_manufacturers = [
    {"name": "SAIC", "country": "China"},
    {"name": "Mitsubishi", "country": "Japan"},
]

manufacturers = [
    {"name": f"name_{num}", "country": f"country_{num}"}
    for num in range(1, MANUFACTURERS_AMOUNT + 1 - len(custom_manufacturers))
] + custom_manufacturers

custom_cars = [
    {"model": "MG 5 II"},
    {"model": "Rising Auto ER6"},
    {"model": "Mitsubishi Eclipse"},
    {"model": "Mitsubishi Lancer"},
]

cars = [
    {"model": f"car_model_{num}"}
    for num in range(1, CARS_AMOUNT + 1 - len(custom_cars))
] + custom_cars

superuser = [
    {
        "username": "admin",
        "password": "admin_password",
        "first_name": "admin_first_name",
        "last_name": "admin_last_name",
        "email": "admin@email.com",
        "license_number": "ADM99999",
    }
]

drivers = [
    {
        "username": f"username_{num}",
        "password": f"password_{num}",
        "first_name": f"first_name_{num}",
        "last_name": f"last_name_{num}",
        "email": f"username_{num}@email.com",
        "license_number": f"NUM{str(num).zfill(DRIVERS_AMOUNT)}",
    }
    for num in range(1, DRIVERS_AMOUNT)
] + superuser


def seed_generator() -> Iterator[int]:
    for seed in itertools.cycle(SEEDS):
        random.seed(seed)
        yield random.randint(1, MANUFACTURERS_AMOUNT + 1)


def fill_db():
    seed = seed_generator()

    Manufacturer.objects.bulk_create(
        [Manufacturer(**manufacturer) for manufacturer in manufacturers]
    )
    Car.objects.bulk_create(
        [Car(**car, manufacturer_id=next(seed)) for car in cars]
    )

    for car in Car.objects.order_by("id")[CARS_AMOUNT - len(custom_cars) :]:
        if car.model.startswith("Mitsubishi"):
            car.manufacturer_id = MANUFACTURERS_AMOUNT
        else:
            car.manufacturer_id = MANUFACTURERS_AMOUNT - 1
        car.save()

    for driver in drivers:
        if driver.get("username") == "admin":
            admin = get_user_model().objects.create_superuser(**driver)
            admin.cars.add(
                *[
                    CARS_AMOUNT - len(custom_cars) + 1,
                    CARS_AMOUNT - len(custom_cars) + 2,
                ]
            )
        else:
            get_user_model().objects.create_user(**driver)
