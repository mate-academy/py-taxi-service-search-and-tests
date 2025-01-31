class UsernameSearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


class ModelSearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        model = self.request.GET.get("model")
        if model:
            return queryset.filter(model__icontains=model)
        return queryset


class NameSearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset
