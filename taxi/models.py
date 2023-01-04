import os.path
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from django.urls import reverse
from django.utils.text import slugify


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


def path_to_image(instance, filename):
    """"""
    _, extension = os.path.splitext(filename)
    if instance.username:
        filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"
        return os.path.join("uploads/avatars/", filename)
    elif instance.model:
        filename = f"{slugify({instance.model})}-{uuid.uuid4()}{extension}"
        return os.path.join("uploads/car_images/", filename)


class Driver(AbstractUser):
    license_number = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to=path_to_image, null=True, blank=True)

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"
        ordering = ("id",)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    user = models.ForeignKey(Driver, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return f"Comment: {self.content} " \
               f"from {self.user.username} " \
               f"at {self.date}"


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer,
                                     on_delete=models.CASCADE)
    drivers = models.ManyToManyField(Driver,
                                     related_name="cars")
    comments = models.ManyToManyField(Comment,
                                      related_name="comments", blank=True)
    image = models.ImageField(null=True,
                              blank=True,
                              upload_to=path_to_image)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.model

    def average_rating(self) -> float:
        return (
            Rating.objects.filter(car=self).aggregate(
                Avg("rating"))["rating__avg"] or 0
        )


class Rating(models.Model):
    user = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.car.model}: {self.rating}"
