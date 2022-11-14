from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("taxi:driver-list")
    else:
        form = RegisterForm()

    context = {
        "form": form,
    }
    return render(request, "register/register.html", context=context)
