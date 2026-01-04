from importlib import import_module

from django.contrib.auth import get_user_model


def create_user_object():
    user = get_user_model().objects.create_user(
        username="TestUser",
        password="password",
    )
    return user


def create_model_instance(model, simple_fields, relational_fields,
                          unique_fields):
    foreign_relation = relational_fields["foreign_relation"]
    many_relation = relational_fields["many_relation"]

    field_data = {field: "Test" for field in simple_fields}
    for field in unique_fields:
        field_data[field] += f"_{model.__name__.lower()}"

    if foreign_relation or many_relation:
        create_related_objects(foreign_relation | many_relation)
        for field_name, related_model in foreign_relation.items():
            field_data[field_name] = related_model.objects.first()

    if model == get_user_model():
        model_instance = get_user_model().objects.create_user(**field_data)
    else:
        model_instance = model.objects.create(**field_data)

    for field_name, related_model in many_relation.items():
        getattr(model_instance, field_name).add(related_model.objects.first())

    model_instance.save()

    return model_instance


def build_context_name(model_name, view_type):
    return f"{model_name}_{view_type}"


def bulk_create_model_instances(
        model, simple_fields, relational_fields, unique_fields
):
    # 7 instances to create enough data to test pagination
    # Search is tested against "test2"
    for i in range(7):
        test = "" if i < 3 else "_test2"
        instance = create_model_instance(
            model, simple_fields, relational_fields, unique_fields
        )
        for field in unique_fields:
            unique_field_value = getattr(instance, field)
            setattr(instance, field, unique_field_value + str(i + 1) + test)
        instance.save()


def create_related_objects(relational_fields):
    for model in relational_fields.values():
        if not model.objects.exists():
            model_name = model.__name__.lower()
            module = import_module(
                f"taxi.tests.test_model_views.test_{model_name}_model_views"
            )
            create_model_instance(
                model,
                module.NON_RELATIONAL_FIELDS,
                module.RELATIONAL_FIELDS,
                module.UNIQUE_FIELDS
            )


def fill_out_create_update_forms(field_text, simple_fields, relational_fields):
    form_data = {field: field_text for field in simple_fields}
    for relation in relational_fields.values():
        for field, model in relation.items():
            if field == "password":
                continue
            form_data[field] = model.objects.first().pk
    return form_data
