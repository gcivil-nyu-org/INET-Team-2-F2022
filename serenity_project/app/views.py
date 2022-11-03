from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets
from .models import ScoreTable, ForumPost, Comment
from .serializers import ScoreTableSerializer
from django.template import RequestContext, Template, Context
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponseRedirect
from django.template.response import TemplateResponse
from .forms import RatingForm, NewUserForm, CreateInForumPost, CreateInComment

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


@login_required(login_url="/login")
def submit_rating(request):
    # csrfContext = RequestContext(request)
    zip = request.POST.get("zip")
    form = RatingForm(request.POST)
    print(zip)
    return render(request, "app/rate.html", {"form": form, "zip": zip})


def update_user_rating(total, grade):
    print(grade)
    if grade == "A":
        total += 1
    if grade == "B":
        total += 2
    if grade == "C":
        total += 3
    if grade == "D":
        total += 4
    if grade == "E":
        total += 5
    if grade == "F":
        total += 6
    if grade == "G":
        total += 7
    return total


@login_required(login_url="/login")
def get_rating(request):
    # csrfContext = RequestContext(request)
    form = RatingForm(request.POST)
    if request.method == "POST":
        form = RatingForm(request.POST)
        zip = request.POST.get("zip")
        grade = request.POST.get("user_rating")
        post = ScoreTable.objects.get(zipcode=zip)
        post.gradeCount += 1
        count = post.gradeCount
        total = post.userGrade
        post.userGrade = update_user_rating(total, grade)
        post.userAvg = post.userGrade / count
        post.save()
        return render(
            request,
            "app/thanks.html",
            {"grade": grade, "zipcode": zip, "updated_grade": post.userAvg},
        )
    return render(request, "app/thanks.html", {"form": form})


def register_request(request):
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


def forum_home(request):
    forumPosts = ForumPost.objects.all()
    count = forumPosts.count()
    comments = []
    for i in forumPosts:
        comments.append(i.comment_set.all())
    context = {"forumPosts": forumPosts, "count": count, "comments": comments}
    return render(request, "app/forum_home.html", context)


def zipcode_forum(request):
    forumPosts = ForumPost.objects.all()
    zipcodes = ScoreTable.objects.all()
    count = zipcodes.count()
    context = {"forumPosts": forumPosts, "count": count, "zipcodes": zipcodes}
    return render(request, "app/zipcode_forum.html", context)



@login_required(login_url="/login")
def addInForumPost(request):
    form = CreateInForumPost()
    if request.method == "POST":
        form = CreateInForumPost(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/forumPosts")
    context = {"form": form}
    return render(request, "app/addInForumPost.html", context)


@login_required(login_url="/login")
def addInComment(request):
    form = CreateInComment()
    if request.method == "POST":
        form = CreateInComment(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/forumPosts")
    context = {"form": form}
    return render(request, "app/addInComment.html", context)


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def internal_error_view(request):
    return render(request, "500.html", status=500)
