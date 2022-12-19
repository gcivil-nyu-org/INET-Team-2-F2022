from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets
from django import forms
from .models import ScoreTable, ForumPost, Comment, Profile
from .serializers import ScoreTableSerializer
from django.template import RequestContext, Template, Context
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponseRedirect, redirect
from django.template.response import TemplateResponse
from .forms import (
    RatingForm,
    NewUserForm,
    CreateInForumPost,
    CreateInComment,
    UpdateUserForm,
    UpdateProfileForm,
)
from django.shortcuts import render

import os
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.contrib.auth import get_user
from scipy.stats import percentileofscore
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


# from .changedata import changemap


class ScoreTableViewSet(viewsets.ModelViewSet):
    queryset = ScoreTable.objects.all()
    serializer_class = ScoreTableSerializer
    http_method_names = ["get", "post"]


def index(request):

    # Steps to update map:
    # 1) Uncomment the below code within this function
    # 2) Go to index.html line ~331 and change the Var APILink to local
    # 3) Runserver manage.py and refresh the home page
    # 4) Undo steps 1 and 2 before pushing code, include db.sqlite3 file in push

    # allposts = ScoreTable.objects.all()
    # scores = []
    # for post in allposts:
    #     score = calculate_factor(post.zipcode)[0]  # only getting score
    #     scores.append(score)
    # for post in allposts:
    #     curr_score = calculate_factor(post.zipcode)[0]
    #     sorted_scores = sorted(scores)
    #     post.grade = _get_grade_from_score(percentileofscore(sorted_scores, curr_score))
    #     post.save()
    return render(request, "app/index.html", {})


def get_info(request):
    return render(request, "app/about.html", {})


def calculate_factor(zipcode):
    zipcodeFactors = ScoreTable.objects.get(zipcode=zipcode)
    n = []
    weights = []
    nFactors = []
    factors = (
        ("residentialNoise", 1),
        ("dirtyConditions", 0.6),
        ("sanitationCondition", 0.6),
        ("wasteDisposal", 0.6),
        ("unsanitaryCondition", 0.6),
        ("constructionImpact", 1),
        ("userAvg", 1),
        ("treeCensus", -1),
        ("parkCount", -1),
    )
    score = 0
    for factor, weight in factors:
        currSet = ScoreTable.objects.values_list(factor, flat=True)
        arr = np.array(currSet)
        # normal = 3 * (getattr(zipcodeFactors, factor) / np.linalg.norm(arr))
        arr_sorted = np.sort(arr)
        normal = percentileofscore(arr_sorted, getattr(zipcodeFactors, factor))
        nFactors.append(round(normal, 2))

        if factor == "userAvg":
            currUserScore = getattr(zipcodeFactors, factor)
        elif factor != "userAvg" and normal != 0:
            n.append(normal)
            weights.append(weight)

    score = np.dot(n, weights)
    if currUserScore != 0:
        score = round((score + currUserScore) / sum(weights), 2)
    else:
        score = round(score / (sum(weights) - 1), 2)
    return score, nFactors


def _get_grade_from_score(score):
    grade = "N"
    if score >= 90:
        grade = "F"
    elif score < 90 and score >= 75:
        grade = "E"
    elif score < 75 and score >= 60:
        grade = "D"
    elif score < 60 and score >= 40:
        grade = "C"
    elif score < 40 and score >= 15:
        grade = "B"
    elif score < 15 and score >= 0:
        grade = "A"
    return grade


def search(request, test=False):  # pragma: no cover
    csrfContext = RequestContext(request)
    if request.method == "POST":
        search = request.POST["searched"]
        try:
            post = ScoreTable.objects.get(zipcode=search)
            parkCountPoint = post.parkCount
            treeCensusPoint = post.treeCensus
            residentialNoisePoint = post.residentialNoise
            dirtyConditionsPoint = post.dirtyConditions
            # norm_score, normals = calculate_factor(search)
            # factors = (
            #     "residentialNoise",
            #     "dirtyConditions",
            #     "sanitationCondition",
            #     "wasteDisposal",
            #     "unsanitaryCondition",
            #     "constructionImpact",
            #     "userAvg",
            #     "treeCensus",
            #     "parkCount",
            # )
            # count = 0
            # for factor in factors:
            #     if factor != "userAvg":
            #         setattr(post, factor, normals[count])
            #         count += 1
            #     else:
            #         count += 1
            # post.raw = norm_score
            # post.grade = _get_grade_from_score(norm_score)
            # post.save()
            rounded = round(post.userAvg, 2)

            constructionImpact = []
            residentialNoise = []
            dirtyConditions = []
            sanitationCondition = []
            wasteDisposal = []
            unsanitaryCondition = []
            treeCensus = []
            parkCount = []
            grade = []
            allposts = ScoreTable.objects.all()
            for row in allposts:
                constructionImpact.append(row.constructionImpact)
                residentialNoise.append(row.residentialNoise)
                dirtyConditions.append(row.dirtyConditions)
                sanitationCondition.append(row.sanitationCondition)
                wasteDisposal.append(row.wasteDisposal)
                unsanitaryCondition.append(row.unsanitaryCondition)
                treeCensus.append(row.treeCensus)
                parkCount.append(row.parkCount)
                grade.append(row.grade)

            path = os.getcwd()
            parent = os.path.dirname(path)
            width = 300
            height = 250
            paper_bg = "#68B984"

            if not test:
                data = pd.read_csv("app/data/tree.csv")
                px.set_mapbox_access_token(
                    "pk.eyJ1IjoiYWJoaWRhc2FyaTEyODkiLCJhIjoiY2xiNXloZnI2MGJkajNwbXF4ZmVxNzJvdCJ9.60A0wnYJlzI-vUcTMUkU5Q"
                )
                source = data[data["zipcode"] == int(search)]
                zipmap = px.scatter_mapbox(
                    source,
                    lat=source.Latitude,
                    lon=source.longitude,
                    color_discrete_sequence=["green"],
                    zoom=16,
                )
                zipmap.update_layout(
                    width=600,
                    height=500,
                    title_text="Tree Mapper",
                    margin=dict(l=20, r=20, t=50, b=20),
                    showlegend=False,
                    paper_bgcolor=paper_bg,
                    mapbox=dict(
                        pitch=60,
                    ),
                )
                zipmap.update_layout(
                    mapbox_style="mapbox://styles/abhidasari1289/clb67vwkt000214mkgynh4pb7"
                )

                group_labels = ["Park Count"]
                park_div = ff.create_distplot(
                    [parkCount], group_labels, colors=["#FF33E9"]
                )

                park_div.update_traces(
                    x=[parkCountPoint],
                    marker=dict(
                        color="red", line=dict(width=5, color="DarkSlateGrey"), size=12
                    ),
                    selector=dict(mode="markers"),
                )
                park_div.update_layout(
                    width=width,
                    height=height,
                    title_text="Park Count Distribution",
                    template="plotly",
                    margin=dict(l=20, r=20, t=50, b=20),
                    showlegend=False,
                    paper_bgcolor=paper_bg,
                )

                # park_div.update_yaxes(visible=False, showticklabels=True)

                group_labels = ["Tree Count"]

                tree_div = ff.create_distplot(
                    [treeCensus], group_labels, bin_size=100, colors=["#FFC300"]
                )

                tree_div.update_traces(
                    x=[treeCensusPoint],
                    marker=dict(
                        color="red", line=dict(width=5, color="DarkSlateGrey"), size=12
                    ),
                    selector=dict(mode="markers"),
                )
                tree_div.update_layout(
                    width=width,
                    height=height,
                    title_text="Tree Count Distribution",
                    template="plotly",
                    margin=dict(l=20, r=20, t=50, b=20),
                    showlegend=False,
                    paper_bgcolor=paper_bg,
                )

                group_labels = ["Residential Noise"]
                res_div = ff.create_distplot(
                    [residentialNoise], group_labels, bin_size=10, colors=["#9C33FF"]
                )

                res_div.update_traces(
                    x=[residentialNoisePoint],
                    marker=dict(
                        color="red", line=dict(width=5, color="DarkSlateGrey"), size=12
                    ),
                    selector=dict(mode="markers"),
                )
                res_div.update_layout(
                    width=width,
                    height=height,
                    title_text="Residential Noise Distribution",
                    template="plotly",
                    margin=dict(l=20, r=20, t=50, b=20),
                    showlegend=False,
                    paper_bgcolor=paper_bg,
                )

                group_labels = ["Dirty Conditions"]
                dirty_div = ff.create_distplot(
                    [dirtyConditions], group_labels, colors=["#C70039"]
                )

                dirty_div.update_traces(
                    x=[dirtyConditionsPoint],
                    marker=dict(
                        color="red", line=dict(width=5, color="DarkSlateGrey"), size=12
                    ),
                    selector=dict(mode="markers"),
                )
                dirty_div.update_layout(
                    width=width,
                    height=height,
                    title_text="Dirty Conditions Distribution",
                    template="plotly",
                    margin=dict(l=20, r=20, t=50, b=20),
                    showlegend=False,
                    paper_bgcolor=paper_bg,
                )

                return render(
                    request,
                    "app/search.html",
                    {
                        "post": post,
                        "rounded": rounded,
                        "plot_div": park_div.to_html(full_html=False),
                        "plot_div1": tree_div.to_html(full_html=False),
                        "plot_div2": res_div.to_html(full_html=False),
                        "plot_div3": dirty_div.to_html(full_html=False),
                        "plot_div4": zipmap.to_html(full_html=False),
                    },
                )
            else:
                return render(request, "app/search.html", {"post": post})
        except ScoreTable.DoesNotExist:
            print("entered else")
            messages.error(
                request, "Invalid NYC zipcode OR We don't have data for this zipcode."
            )
            return render(request, "app/index.html", {})
    else:
        # return render(request, "app/search.html", {}, csrfContext)
        return redirect("home")


def find(request):
    find = request.POST["find"]
    try:
        one_entry = ScoreTable.objects.get(zipcode=find)
    except:
        messages.error(
            request, "Invalid NYC zipcode OR We don't have data for this zipcode."
        )
        return render(request, "app/forum_home.html", {})
    return redirect("forum_zipcode", pk=find)


@login_required(login_url="/login")
def submit_rating(request):
    # csrfContext = RequestContext(request)
    if request.method == "POST":
        zip = request.POST.get("zip")
        form = RatingForm(request.POST)
        return render(request, "app/rate.html", {"form": form, "zip": zip})
    return redirect("home")


def update_user_rating(total, grade):
    if grade == "A":
        total += 7.5
    if grade == "B":
        total += 25
    if grade == "C":
        total += 50
    if grade == "D":
        total += 67.5
    if grade == "E":
        total += 82.5
    if grade == "F":
        total += 95

    return total


@login_required(login_url="/login")
def get_rating(request):
    # csrfContext = RequestContext(request)
    form = RatingForm(request.POST)
    if request.method == "POST":
        form = RatingForm(request.POST)
        zip = request.POST.get("zip")
        grade = request.POST.get("user_rating")
        if isinstance(grade, str) and len(grade) == 1:
            if (
                grade == "A"
                or grade == "B"
                or grade == "C"
                or grade == "D"
                or grade == "E"
                or grade == "F"
            ):
                post = ScoreTable.objects.get(zipcode=zip)
                post.gradeCount += 1
                count = post.gradeCount
                total = post.userGrade
                post.userGrade = update_user_rating(total, grade)
                post.userAvg = post.userGrade / count
                post.save()
                score = calculate_factor(zipcode=zip)[0]  # only getting score
                post.grade = _get_grade_from_score(score)
                post.save()
                return render(
                    request,
                    "app/thanks.html",
                    {"grade": grade, "zipcode": zip, "updated_grade": post.userAvg},
                )
            else:
                messages.error(request, "Invalid grade! Try again!")
                return render(request, "app/rate.html", {"form": form, "zip": zip})
    return render(request, "app/rate.html", {"form": form, "zip": zip})


def register_request(request):
    if not request.user.is_anonymous:
        return redirect("home")
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
    if not request.user.is_anonymous:
        return redirect("home")
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
    # TODO: show all buroughs
    boroughs = ["Manhattan", "Brooklyn", "Staten Island", "Queens", "Bronx"]
    context = {"boroughs": boroughs}
    return render(request, "app/forum_home.html", context)


def forum_borough(request, borough):
    # TODO: show zipcodes filtered by burough
    boroughs = ["Manhattan", "Brooklyn", "Staten Island", "Queens", "Bronx"]
    if borough not in boroughs:
        return render(request, "404.html", status=404)
    forumPosts = ForumPost.objects.all()
    forumPosts = forumPosts.filter(zipcode__borough=borough)
    zipcodes = set()
    for post in forumPosts:
        zipcodes.add(post.zipcode.zipcode)
    count = len(zipcodes)
    context = {
        "borough": borough,
        "zipcodes": zipcodes,
        "count": count,
    }
    return render(request, "app/forum_borough.html", context)


def forum_zipcode(request, pk):
    posts = ForumPost.objects.all()
    posts = posts.filter(zipcode__zipcode=pk)
    count = posts.count()
    comments = []
    for i in posts:
        comments.append(i.comment_set.all())
    context = {
        "zipcode": pk,
        "forumPosts": posts,
        "count": count,
        "comments": comments,
    }

    allZips = ScoreTable.objects.all()
    checkZip = allZips.filter(zipcode=pk)
    if len(checkZip) == 0:
        return render(request, "404.html", status=404)
    return render(request, "app/forum_zipcode.html", context)


def forum_post(request, pk, id):
    id = int(id)
    posts = ForumPost.objects.all()
    posts = posts.filter(zipcode__zipcode=pk)
    comments = []
    for i in posts:
        comments.append(i.comment_set.all())
    context = {
        "zipcode": pk,
        "forumPosts": posts,
        "comments": comments,
        "id": id,
    }

    checkId = posts.filter(id=id)
    if len(checkId) == 0:
        return render(request, "404.html", status=404)

    return render(request, "app/forum_post.html", context)


def _zipcode_to_id(zipcode):
    table = ScoreTable.objects.get(zipcode=zipcode)
    return table.id


@login_required(login_url="/login")
def addInForumPost(request):
    form = CreateInForumPost()
    if request.method == "POST":
        form = CreateInForumPost(request.POST)
        if form.is_valid():
            form.save()
            current_zip = form.cleaned_data["zipcode"]
            form.save()
            return redirect(f"/forumPosts/zipcode/{current_zip}/")

    curzip = "11205"
    if "curzip" in request.POST:
        curzip = request.POST["curzip"]

    user = get_user(request)
    email = user.email
    form = CreateInForumPost(
        initial={"name": user, "email": email, "zipcode": _zipcode_to_id(int(curzip))}
    )
    form.fields["name"].widget = forms.HiddenInput()
    form.fields["email"].widget = forms.HiddenInput()
    context = {"form": form, "user": user, "email": email}
    return render(request, "app/addInForumPost.html", context)


@login_required(login_url="/login")
def addInComment(request):
    form = CreateInComment()
    if request.method == "POST":
        form = CreateInComment(request.POST)
        if form.is_valid():
            form.save()
            current_zip = form.cleaned_data["forumPost"]
            current_zip = current_zip.zipcode
            post_id = form["forumPost"].value()
            return redirect(f"/forumPosts/zipcode/{current_zip}/{post_id}/")

    curpost = "1"
    if "post" in request.POST:
        curpost = request.POST["post"]

    user = get_user(request)
    email = user.email
    form = CreateInComment(initial={"name": user, "email": email, "forumPost": curpost})
    form.fields["name"].widget = forms.HiddenInput()
    form.fields["email"].widget = forms.HiddenInput()
    context = {"form": form, "user": user, "email": email}
    return render(request, "app/addInComment.html", context)


@login_required
def profile(request):
    # ?: list all the posts
    posts = ForumPost.objects.filter(name=request.user)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if profile_form.is_valid():
            # user_form.save()
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect(to="profile")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(
        request,
        "app/users/profile.html",
        {"user_form": user_form, "profile_form": profile_form, "forumPosts": posts},
    )


def get_others(request, name):
    # ?: list all the posts
    posts = ForumPost.objects.filter(name=name)

    try:
        profile = Profile.objects.get(user__username=name)
        return render(
            request,
            "app/users/other_profile.html",
            {"username": name, "profile": profile, "forumPosts": posts},
        )

    except:
        return render(request, "404.html", status=404)


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def internal_error_view(request):
    return render(request, "500.html", status=500)
