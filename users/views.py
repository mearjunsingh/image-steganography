from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_user(request):
    if request.user.is_authenticated:
        return redirect("/user/")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        new_user = form.save()
        new_user.is_staff = True
        new_user.save()
        messages.info(request, "Thanks for registering. You are now logged in.")
        new_user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(request, new_user)
        return redirect("/")
    return render(request, "register.html", {"form": form})
