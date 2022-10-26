from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets
from .models import ScoreTable
from .serializers import ScoreTableSerializer
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext, Template, Context
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


from django.template.response import TemplateResponse


import pandas as pd
import numpy as np


class ScoreTableViewSet(viewsets.ModelViewSet):
    queryset = ScoreTable.objects.all()
    serializer_class = ScoreTableSerializer


def index(request):
    latest_zipcode_list = ScoreTable.objects.order_by("zipcode")[:5]
    context = {"latest_zipcode_list": latest_zipcode_list}
    return render(request, "app/index.html", context)


def search(request):
    csrfContext = RequestContext(request)
    if request.method == "POST":
        search = request.POST["searched"]
        post = ScoreTable.objects.get(zipcode=search)
        # currZip = post.zipcode
        normalizeNoise = (
            post.residentialNoise
            + post.dirtyConditions
            + post.sanitationCondition
            + post.wasteDisposal
            + post.unsanitaryCondition
        ) / 1000
        if normalizeNoise >= 7:
            post.grade = "G"
        elif normalizeNoise < 7 and normalizeNoise >= 6:
            post.grade = "G"
        elif normalizeNoise < 6 and normalizeNoise >= 5:
            post.grade = "E"
        elif normalizeNoise < 5 and normalizeNoise >= 4:
            post.grade = "D"
        elif normalizeNoise < 4 and normalizeNoise >= 3:
            post.grade = "C"
        elif normalizeNoise < 3 and normalizeNoise >= 2:
            post.grade = "B"
        elif normalizeNoise < 2 and normalizeNoise >= 0:
            post.grade = "A"
        post.residential_Noise = normalizeNoise
        return render(request, "app/search.html", {"post": post})
    else:
        return render(request, "app/search.html", {}, csrfContext)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="app/register.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="app/login.html", context={"login_form": form}
    )


def map_view(request):
    return render(request, "app/map.html", {})
