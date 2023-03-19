from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import BankSoal
import json
import random
from string import ascii_lowercase as alc


def bank_soal_serializer(pk):
    if pk == "all":
        data = serializers.serialize("json", BankSoal.objects.all())
    else:
        data = serializers.serialize(
            "json", [BankSoal.objects.filter(status=1).get(pk=pk)])
    temp_json = json.loads(data)
    data_json = {}

    for item in temp_json:
        id = str(item["pk"])
        data_json[id] = item["fields"]
        
        try:
            data_json[id]["choices"] = json.loads(data_json[id]["choices"])
        except:
            data_json[id]["choices"] = json.loads(data_json[id]["choices"].replace("\'","\""))

        if data_json[id]["answer"][0] == "{" and data_json[id]["answer"][-1] == "}":
            try:
                data_json[id]["answer"] = json.loads(data_json[id]["answer"])
            except:
                data_json[id]["answer"] = json.loads(data_json[id]["answer"].replace("\'","\""))

    return data_json


def get_question(question_id):
    question = bank_soal_serializer(question_id)[question_id]
    key_choices = [alc[i].upper() for i in range(len(question["choices"]))]
    random.shuffle(question["choices"])
    question["choices"] = {key_choices[i]: question["choices"][i]
                           for i in range(len(key_choices))}
    return question


def render_quiz(request):
    return render(request, "quiz.html")


def render_result(request):
    try:
        context = request.session['quiz']
    except:
        context = { "score": 0,
                    "answerHistory": {"correct": 0, "wrong": 0, "empty": 0},
                    "progress": 0,
                    }
    return render(request, "result.html", context)


def reset(request):
    try:
        request.session.pop('quiz')
    except:
        pass
    return redirect(render_quiz)

@csrf_exempt
def quiz(request):
    resp = {"status": 405}
    filter = {"sources": sorted(list(set(BankSoal.objects.values_list("source", flat=True))))}
    allQuestionId = list(BankSoal.objects.filter(status=1, source__in=filter["sources"]).values_list("pk", flat=True))
    currQuestionId = random.choice(allQuestionId)
    question = get_question(str(currQuestionId))
    
    if request.method == "GET":
        try:
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
                    "score": request.session["quiz"]["score"],
                    "answerHistory": request.session["quiz"]["answerHistory"],
                    "progress": request.session["quiz"]["progress"],
                    "questionIdTaken": request.session["quiz"]["questionIdTaken"],
                    "allQuestionId": request.session["quiz"]["allQuestionId"],
                    "status": 200,
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
                    "score": 0,
                    "answerHistory": {"correct": 0, "wrong": 0, "empty": 0},
                    "progress": 0,
                    "questionIdTaken": [],
                    "allQuestionId": allQuestionId,
                    "status": 200,
                    }
        
        response = HttpResponse(json.dumps(resp), content_type="application/json")
        response.status_code = 200
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
            score = userData["score"]
            answerHistory["empty"] = answerHistory["empty"]+1

        if isCorrect:
            score = userData["score"]+1
            answerHistory["correct"] = answerHistory["correct"]+1
        else:
            if userData["userAnswer"]:
                score = userData["score"]
                answerHistory["wrong"] = answerHistory["wrong"]+1

        questionIdTaken = userData["questionIdTaken"]+[currQuestionId]
        allQuestionId =  userData["allQuestionId"]
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
                "score": score,
                "answerHistory": answerHistory,
                "progress": progress,
                "questionIdTaken":  questionIdTaken,
                "allQuestionId": allQuestionId,
                "status": 200,
                }
        request.session['quiz'] = resp
        response = HttpResponse(json.dumps(resp), content_type="application/json")
        response.status_code = 200
        return response
    
    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response.status_code = 405
    return response


@csrf_exempt
def shuffle(request):
    resp = {"status": 405}
    if request.method == "POST":
        userData = json.loads(request.body)
        allQuestionId = userData["allQuestionId"]
        questionIdTaken = userData["questionIdTaken"]
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
                "score": userData["score"],
                "answerHistory": userData["answerHistory"],
                "progress": userData["progress"],
                "questionIdTaken": questionIdTaken,
                "allQuestionId": allQuestionId,
                "status": 200,
                }
        
        response = HttpResponse(json.dumps(resp), content_type="application/json")
        response.status_code = 200
        return response
    
    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response.status_code = 405
    return response

@csrf_exempt
def filter(request):
    resp = {"status": 405}
    if request.method == "POST":
        userData = json.loads(request.body)
        
        activeFilter = userData["activeFilter"]
        for key in activeFilter:
            if len(activeFilter[key]) == 0:
                activeFilter[key] = userData["filter"][key]
        
        allQuestionId = list(BankSoal.objects.filter(status=1, source__in=activeFilter["sources"]).values_list("pk", flat=True))
        currQuestionId = random.choice(allQuestionId)
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
                "score": 0,
                "answerHistory": {"correct": 0, "wrong": 0, "empty": 0},
                "progress": 0,
                "questionIdTaken": [],
                "allQuestionId": allQuestionId,
                "status": 200,
                }
        
        request.session['quiz'] = resp
        response = HttpResponse(json.dumps(resp), content_type="application/json")
        response.status_code = 200
        return response
        
    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response.status_code = 405
    return response


