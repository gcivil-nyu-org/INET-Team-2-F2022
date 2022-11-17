import json
import numpy as np
import requests
from django.contrib.staticfiles.storage import staticfiles_storage

# from django.conf.urls.static import static


MAP_PATH = staticfiles_storage.path("json/sample.geojson")
# MAP_PATH = static('/static/json/sample.geojson')[0]
response = requests.get(
    "http://se-proj-develop-env.eba-yiphn7ci.us-west-2.elasticbeanstalk.com/api/table/"
)
data = response.json()


def set_of_factor(data, factor):
    ans = []
    for piece in data:
        ans.append(piece[factor])
    return ans


def calculate_factor(data, datapiece):
    # zipcodeFactors = ScoreTable.objects.get(zipcode=zipcode)
    curpiece = datapiece
    n = []
    weights = []
    nFactors = []
    factors = (
        "residentialNoise",
        "dirtyConditions",
        "sanitationCondition",
        "wasteDisposal",
        "unsanitaryCondition",
        "constructionImpact",
        "userAvg",
    )
    for factor in factors:
        # currSet = ScoreTable.objects.values_list(factor, flat=True)
        currSet = set_of_factor(data, factor)
        arr = np.array(currSet)
        # normal = getattr(zipcodeFactors, factor) / np.linalg.norm(arr)
        normal = curpiece[factor] / np.linalg.norm(arr)

        nFactors.append(round(normal, 2))
        if normal != 0:
            n.append(normal)
            if factor == "constructionImpact":
                weights.append(4)
            elif factor == "userAvg":
                weights.append(0.5)
            else:
                weights.append(1)
    n = np.array(n)
    weights = np.array(weights)
    score = round(np.average(n, weights=weights), 2)
    return score, nFactors


def _get_grade_from_score(score):
    grade = None
    if score >= 0.4:
        grade = "G"
    elif score < 0.4 and score >= 0.3:
        grade = "F"
    elif score < 0.3 and score >= 0.2:
        grade = "E"
    elif score < 0.2 and score >= 0.15:
        grade = "D"
    elif score < 0.15 and score >= 0.1:
        grade = "C"
    elif score < 0.1 and score >= 0.05:
        grade = "B"
    elif score < 0.05 and score >= 0:
        grade = "A"
    return grade


def changemap():
    grade_dic = {}
    for piece in data:
        score, nFactors = calculate_factor(data, piece)
        grade_dic[piece["zipcode"]] = _get_grade_from_score(score)
        # print(_get_grade_from_score(score))

    # change mapdata with new grades
    print(MAP_PATH)
    f = open(MAP_PATH)
    mapdata = json.load(f)
    f.close()

    for i in range(len(mapdata["features"])):
        curpiece = mapdata["features"][i]["properties"]
        zipcode = curpiece["postalCode"]
        if zipcode in grade_dic:
            curpiece["grade"] = grade_dic[zipcode]

    with open(MAP_PATH, "w") as outfile:
        json.dump(mapdata, outfile)
