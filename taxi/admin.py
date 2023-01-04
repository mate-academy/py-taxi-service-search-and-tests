from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Driver, Car, Manufacturer, Comment


@admin.register(Driver)
class DriverAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("license_number",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("license_number", "avatar")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "license_number",
                        "avatar",
                    )
                },
            ),
        )
    )


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    search_fields = ("model",)
    list_filter = ("manufacturer",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "content",
    )
    list_filter = ("user",)
    search_fields = (
        "user",
        "content",
    )


admin.site.register(Manufacturer)
