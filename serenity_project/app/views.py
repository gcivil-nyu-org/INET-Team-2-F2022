from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets
from django import forms
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
from django.http import HttpResponse
from django.contrib.auth import get_user
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


# from .changedata import changemap


class ScoreTableViewSet(viewsets.ModelViewSet):
    queryset = ScoreTable.objects.all()
    serializer_class = ScoreTableSerializer
    http_method_names = ["get"]


def index(request):

    #Steps to update map:
    # 1) Uncomment the below code within this function
    # 2) Go to index.html line ~331 and change the Var APILink to local
    # 3) Runserver manage.py and refresh the home page
    # 4) Undo steps 1 and 2 before pushing code, include db.sqlite3 file in push
    

    # allposts = ScoreTable.objects.all()
    # for post in allposts:
    #     score = calculate_factor(post.zipcode)[0] #only getting score
    #     post.grade = _get_grade_from_score(score)
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
        ("dirtyConditions", 1),
        ("sanitationCondition", 1),
        ("wasteDisposal", 1),
        ("unsanitaryCondition", 1),
        ("constructionImpact", 4),
        ("userAvg", 1),
        ("treeCensus", -0.5),
        ("parkCount", -1),
    )
    score = 0
    for factor, weight in factors:
        currSet = ScoreTable.objects.values_list(factor, flat=True)
        arr = np.array(currSet)
        normal = 3 * (getattr(zipcodeFactors, factor) / np.linalg.norm(arr))
        nFactors.append(round(normal, 2))
        if factor == "userAvg":
            currUserScore = getattr(zipcodeFactors, factor)
        elif factor != "userAvg" and normal != 0:
            n.append(normal)
            weights.append(weight)
    score = round(np.average(n, weights=weights), 2)
    if currUserScore != 0:
        if currUserScore > score:
            score = round(((score + (0.5 * currUserScore)) / 2), 2)
        else:
            score = round(((score - (0.5 * currUserScore)) / 2), 2)
    return score, nFactors


def _get_grade_from_score(score):
    grade = "N"
    if score >= 0.6:
        grade = "G"
    elif score < 0.6 and score >= 0.5:
        grade = "F"
    elif score < 0.5 and score >= 0.4:
        grade = "E"
    elif score < 0.4 and score >= 0.3:
        grade = "D"
    elif score < 0.3 and score >= 0.2:
        grade = "C"
    elif score < 0.2 and score >= 0.1:
        grade = "B"
    elif score < 0.1 and score >= 0:
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
            norm_score, normals = calculate_factor(search)
            factors = (
                "residentialNoise",
                "dirtyConditions",
                "sanitationCondition",
                "wasteDisposal",
                "unsanitaryCondition",
                "constructionImpact",
                "userAvg",
                "treeCensus",
                "parkCount",
            )
            count = 0
            for factor in factors:
                if factor != "userAvg":
                    setattr(post, factor, normals[count])
                    count += 1
                else:
                    count += 1
            post.raw = norm_score
            post.grade = _get_grade_from_score(norm_score)
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
            # menu=["constructionImpact","residentialNoise","sanitationCondition","treeCensus","parkCount"]

            # def multiplot(menu):
            #     #fig = ff.create_distplot([constructionImpact,residentialNoise,
            # sanitationCondition,treeCensus,parkCount], menu, bin_size=.2)
            #     dt=[constructionImpact,residentialNoise,sanitationCondition,treeCensus,parkCount]
            #     first_title = menu[0]
            #     traces = []
            #     buttons = []
            #     for i,d in enumerate(menu):
            #         visible = [False] * len(menu)
            #         visible[i] = True
            #         name = d
            #         print(visible)
            #         traces.append(go.Histogram(x=dt[i],visible=True if i==0 else False))
            #         if name == "constructionImpact":
            #              traces.append(go.Histogram(x=constructionImpact, name=name, visible=visible[0]))
            #         elif name == "residentialNoise":
            #              traces.append(go.Histogram(x=residentialNoise, name=name, visible=visible[1]))
            #         elif name == "sanitationCondition":
            #              traces.append(go.Histogram(x=sanitationCondition, name=name, visible=visible[2]))
            #         elif name == "treeCensus":
            #              traces.append(go.Histogram(x=treeCensus, name=name, visible=visible[3]))
            #         elif name == "parkCount":
            #              traces.append(go.Histogram(x=parkCount, name=name,  visible=visible[4]))
            #         buttons.append(dict(label=name,
            #             method="update",
            #             args=[{"title":f"{name}"}]))

            #     updatemenus = [{'active':0, "buttons":buttons}]
            #     print(updatemenus)

            #     fig = go.Figure(data=traces,
            #      layout=dict(updatemenus=updatemenus))
            #     fig.update_layout(title=first_title, title_x=0.5)

            #     #fig = px.histogram(x=treeCensus)
            #     return fig

            # test1=multiplot(menu)
            if not test:
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
                    width=650,
                    height=500,
                    title_text="Park Count Distribution",
                    template="ggplot2",
                )

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
                    width=650,
                    height=500,
                    title_text="Tree Count Distribution",
                    template="ggplot2",
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
                    width=650,
                    height=500,
                    title_text="Residential Noise Distribution",
                    template="ggplot2",
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
                    width=650,
                    height=500,
                    title_text="Dirty Conditions Distribution",
                    template="ggplot2",
                )

                fig = px.scatter_3d(
                    x=np.log(parkCount),
                    y=np.log(treeCensus),
                    z=np.log(residentialNoise),
                    color=grade,
                ).to_html(full_html=False, default_height=500, default_width=500)

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
                        "plot_div4": fig,
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
        total += 0.1
    if grade == "B":
        total += 0.2
    if grade == "C":
        total += 0.3
    if grade == "D":
        total += 0.4
    if grade == "E":
        total += 0.5
    if grade == "F":
        total += 0.6
    if grade == "G":
        total += 0.7
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
                or grade == "G"
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


def _id_to_zipcode(id):
    table = ScoreTable.objects.get(id=id)
    return table.zipcode


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
            return redirect("/forumPosts")

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
            return redirect("/forumPosts")

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


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def internal_error_view(request):
    return render(request, "500.html", status=500)
