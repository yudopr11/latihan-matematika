import json
import random
from string import ascii_lowercase as alc

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render

from .models import BankSoal


headers = {
    "Cache-Control": "no-cache",
}


def bank_soal_serializer(pk):
    data = serializers.serialize("json", [BankSoal.objects.get(pk=pk)])
    data_json = json.loads(data)[0]
    data_json = data_json["fields"]
    try:
            data_json["choices"] = json.loads(data_json["choices"])
    except:
            data_json["choices"] = json.loads(data_json["choices"].replace("\'", "\""))

    if data_json["answer"][0] in ("\'", "\"") and data_json["answer"][-1] in ("\'", "\""):
            data_json["answer"] = data_json["answer"][1:-1]

    if data_json["answer"][0] == "{" and data_json["answer"][-1] == "}":
        try:
            data_json["answer"] = json.loads(data_json["answer"])
        except:
            data_json["answer"] = json.loads(data_json["answer"].replace("\'", "\""))

    return data_json


def get_question(question_id):
    question = bank_soal_serializer(question_id)
    key_choices = [alc[i].upper() for i in range(len(question["choices"]))]
    random.shuffle(question["choices"])
    question["choices"] = {key_choices[i]: question["choices"][i] for i in range(len(key_choices))}
    return question


def render_quiz(request):
    return render(request, "quiz.html")


@require_http_methods(["GET"])
def render_result(request):
    try:
        context = request.session['quiz']
    except:
        context = {"answerHistory": {"correct": 0, "wrong": 0, "empty": 0},
                   "progress": 0,
                   }
    return render(request, "result.html", context)


@require_http_methods(["GET"])
def reset(request):
    try:
        request.session.pop('quiz')
    except:
        pass
    return redirect(render_quiz)


@require_http_methods(["GET", "POST"])
def quiz(request):
    if request.method == "GET":
        filter = {"subject": sorted(list(set(BankSoal.objects.values_list("subject", flat=True)))), 
                  "sources": sorted(list(set(BankSoal.objects.values_list("source", flat=True))))}
        allQuestionId = list(BankSoal.objects.filter(status=1, subject__in=filter["subject"], source__in=filter["sources"]).values_list("pk", flat=True))
        currQuestionId = random.choice(allQuestionId)
        question = get_question(str(currQuestionId))
        try:
            currQuestionId = random.choice(list(set(request.session["quiz"]["allQuestionId"]) - set(request.session["quiz"]["questionIdTaken"])))
            question = get_question(str(currQuestionId))
            if question["status"] == 0:
                request.session["quiz"]["allQuestionId"].remove(currQuestionId)
                currQuestionId = random.choice(list(set(request.session["quiz"]["allQuestionId"]) - set(request.session["quiz"]["questionIdTaken"])))
                question = get_question(str(currQuestionId))

            resp = {"question": {
                "text": question["question"],
                "choices": question["choices"],
                "explanation": question["explanation"],
                "type": question["type"],
                "explanationType": question["explanation_type"],
            },
                "filter": request.session["quiz"]["filter"],
                "activeFilter": request.session["quiz"]["activeFilter"],
                "currQuestionId": currQuestionId,
                "isCorrect": None,
                "answerHistory": request.session["quiz"]["answerHistory"],
                "progress": request.session["quiz"]["progress"],
                "questionIdTaken": request.session["quiz"]["questionIdTaken"],
                "allQuestionId": request.session["quiz"]["allQuestionId"],
            }
        except:
            resp = {"question": {
                "text": question["question"],
                "choices": question["choices"],
                "explanation": question["explanation"],
                "type": question["type"],
                "explanationType": question["explanation_type"],
            },
                "filter": filter,
                "activeFilter": filter,
                "currQuestionId": currQuestionId,
                "isCorrect": None,
                "answerHistory": {"correct": 0, "wrong": 0, "empty": 0},
                "progress": 0,
                "questionIdTaken": [],
                "allQuestionId": allQuestionId,
            }

        response = JsonResponse(resp, headers=headers)
        return response

    if request.method == "POST":
        userData = json.loads(request.body)
        currQuestionId = userData["currQuestionId"]
        question = get_question(str(currQuestionId))

        if userData["question"]["type"] == "tabel-benar-salah":
            userData["userAnswer"] = json.loads(userData["userAnswer"])

        isCorrect = (question["answer"] == userData["userAnswer"])
        answerHistory = userData["answerHistory"]

        if userData["userAnswer"] is None:
            answerHistory["empty"] = answerHistory["empty"]+1

        if isCorrect:
            answerHistory["correct"] = answerHistory["correct"]+1
        else:
            if userData["userAnswer"]:
                answerHistory["wrong"] = answerHistory["wrong"]+1

        questionIdTaken = userData["questionIdTaken"]+[currQuestionId]
        allQuestionId = userData["allQuestionId"]
        progress = len(questionIdTaken)/len(allQuestionId)
        filter = userData["filter"]
        activeFilter = userData["activeFilter"]

        resp = {"question": {
            "text": question["question"],
            "choices": question["choices"],
            "explanation": question["explanation"],
            "type": question["type"],
            "explanationType": question["explanation_type"],
        },
            "filter": filter,
            "activeFilter": activeFilter,
            "currQuestionId": currQuestionId,
            "isCorrect": isCorrect,
            "answerHistory": answerHistory,
            "progress": progress,
            "questionIdTaken":  questionIdTaken,
            "allQuestionId": allQuestionId,
        }
        request.session['quiz'] = resp
        response = JsonResponse(resp, headers=headers)
        return response


@require_http_methods(["POST"])
def shuffle(request):
    if request.method == "POST":
        userData = json.loads(request.body)
        allQuestionId = userData["allQuestionId"]
        questionIdTaken = userData["questionIdTaken"]
        currQuestionId = random.choice(list(set(allQuestionId) - set(questionIdTaken)))
        question = get_question(str(currQuestionId))
        if question["status"] == 0:
            allQuestionId.remove(currQuestionId)
            currQuestionId = random.choice(list(set(allQuestionId) - set(questionIdTaken)))
            question = get_question(str(currQuestionId))

        resp = {"question": {
            "text": question["question"],
            "choices": question["choices"],
            "explanation": question["explanation"],
            "type": question["type"],
            "explanationType": question["explanation_type"],
        },
            "filter": userData["filter"],
            "activeFilter": userData["activeFilter"],
            "currQuestionId": currQuestionId,
            "answerHistory": userData["answerHistory"],
            "progress": userData["progress"],
            "questionIdTaken": questionIdTaken,
            "allQuestionId": allQuestionId,
        }
        response = JsonResponse(resp, headers=headers)
        return response


@require_http_methods(["POST"])
def filter(request):
    if request.method == "POST":
        userData = json.loads(request.body)
        activeFilter = userData["activeFilter"]

        for key in activeFilter:
            if len(activeFilter[key]) == 0:
                activeFilter[key] = userData["filter"][key]
        
        allQuestionId = list(BankSoal.objects.filter(status=1, subject__in=activeFilter["subject"], source__in=activeFilter["sources"]).values_list("pk", flat=True))

        try:
            currQuestionId = random.choice(allQuestionId)
            question = get_question(str(currQuestionId))
        except:
            currQuestionId = None
            question = {"question": None, "choices": None, "explanation": None, "type": None, "explanation_type": None}

        resp = {"question": {
            "text": question["question"],
            "choices": question["choices"],
            "explanation": question["explanation"],
            "type": question["type"],
            "explanationType": question["explanation_type"],
        },
            "filter": userData["filter"],
            "activeFilter": activeFilter,
            "currQuestionId": currQuestionId,
            "answerHistory": {"correct": 0, "wrong": 0, "empty": 0},
            "progress": 0,
            "questionIdTaken": [],
            "allQuestionId": allQuestionId,
        }
        request.session['quiz'] = resp
        response = JsonResponse(resp, headers=headers)
        return response


@login_required
def render_preview(request, pk):
    try:   
        get_question(str(pk))
    except:
        return render(request, "404.html")

    context = {'pk': pk}
    return render(request, "preview.html", context)


@require_http_methods(["GET", "POST"])
@login_required
def preview(request, pk):
    filter = {"subject": sorted(list(set(BankSoal.objects.values_list("subject", flat=True)))), 
              "sources": sorted(list(set(BankSoal.objects.values_list("source", flat=True))))}
    allQuestionId = list(BankSoal.objects.values_list("pk", flat=True))
    currQuestionId = pk
    question = get_question(str(currQuestionId))

    if request.method == "GET":
        resp = {"question": {
            "text": question["question"],
            "choices": question["choices"],
            "explanation": question["explanation"],
            "type": question["type"],
            "explanationType": question["explanation_type"],
        },
            "filter": filter,
            "activeFilter": filter,
            "currQuestionId": currQuestionId,
            "isCorrect": None,
            "answerHistory": {"correct": 0, "wrong": 0, "empty": 0},
            "progress": 0,
            "questionIdTaken": [],
            "allQuestionId": allQuestionId,
        }

        response = JsonResponse(resp, headers=headers)
        return response

    if request.method == "POST":
        userData = json.loads(request.body)
        currQuestionId = userData["currQuestionId"]
        question = get_question(str(currQuestionId))

        if userData["question"]["type"] == "tabel-benar-salah":
            userData["userAnswer"] = json.loads(userData["userAnswer"])

        isCorrect = (question["answer"] == userData["userAnswer"])
        answerHistory = userData["answerHistory"]

        if userData["userAnswer"] is None:
            answerHistory["empty"] = answerHistory["empty"]+1

        if isCorrect:
            answerHistory["correct"] = answerHistory["correct"]+1
        else:
            if userData["userAnswer"]:
                answerHistory["wrong"] = answerHistory["wrong"]+1

        questionIdTaken = userData["questionIdTaken"]+[currQuestionId]
        allQuestionId = userData["allQuestionId"]
        progress = len(questionIdTaken)/len(allQuestionId)
        filter = userData["filter"]
        activeFilter = userData["activeFilter"]

        resp = {"question": {
            "text": question["question"],
            "choices": question["choices"],
            "explanation": question["explanation"],
            "type": question["type"],
            "explanationType": question["explanation_type"],
        },
            "filter": filter,
            "activeFilter": activeFilter,
            "currQuestionId": currQuestionId,
            "isCorrect": isCorrect,
            "answerHistory": answerHistory,
            "progress": progress,
            "questionIdTaken":  questionIdTaken,
            "allQuestionId": allQuestionId,
        }
        response = response = JsonResponse(resp, headers=headers)
        return response
