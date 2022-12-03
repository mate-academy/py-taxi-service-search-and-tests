from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):
    avatar = models.ImageField(null=True, blank=True, default="default.png")
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.username} ({self.first_name} {self.last_name})"
        return self.username

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(Driver, related_name="cars")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.model


class CarComments(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="comments_car"
    )
    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, default=None, blank=True, null=True
    )
    text = models.TextField(verbose_name="text")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Driver, related_name="car_comment")

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.driver.username} left the comment {self.text[:10]}..."
