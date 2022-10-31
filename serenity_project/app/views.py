from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets
from .models import ScoreTable
from .serializers import ScoreTableSerializer
from django.template import RequestContext, Template, Context
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponseRedirect
from django.template.response import TemplateResponse

import pandas as pd
import numpy as np


class ScoreTableViewSet(viewsets.ModelViewSet):
    queryset = ScoreTable.objects.all()
    serializer_class = ScoreTableSerializer


def index(request):
    return render(request, "app/index.html", {})


def _get_city_normalized_noise(
    resident_noise,
    dirty_conditions,
    sanitation_condition,
    waste_disposal,
    unsanitary_condition,
):
    return (
        resident_noise
        + dirty_conditions
        + sanitation_condition
        + waste_disposal
        + unsanitary_condition
    ) / 1000


def _get_city_grade_from_noise(normalized_noise):
    grade = None
    if normalized_noise >= 7:
        grade = "G"
    elif normalized_noise < 7 and normalized_noise >= 6:
        grade = "F"
    elif normalized_noise < 6 and normalized_noise >= 5:
        grade = "E"
    elif normalized_noise < 5 and normalized_noise >= 4:
        grade = "D"
    elif normalized_noise < 4 and normalized_noise >= 3:
        grade = "C"
    elif normalized_noise < 3 and normalized_noise >= 2:
        grade = "B"
    elif normalized_noise < 2 and normalized_noise >= 0:
        grade = "A"
    return grade


def search(request):  # pragma: no cover
    csrfContext = RequestContext(request)
    if request.method == "POST":
        search = request.POST["searched"]
        post = ScoreTable.objects.get(zipcode=search)
        # currZip = post.zipcode
        normalizeNoise = _get_city_normalized_noise(
            post.residentialNoise,
            post.dirtyConditions,
            post.sanitationCondition,
            post.wasteDisposal,
            post.unsanitaryCondition,
        )

        post.overallScore = normalizeNoise
        post.grade = _get_city_grade_from_noise(normalizeNoise)

        return render(request, "app/search.html", {"post": post})
    else:
        return render(request, "app/search.html", {}, csrfContext)


def register_request(request):  # pragma: no cover
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="app/register.html",
        context={"register_form": form},
    )


def login_request(request):  # pragma: no cover
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="app/login.html", context={"login_form": form}
    )


def logoutUser(request):
    logout(request)
    return redirect("home")
