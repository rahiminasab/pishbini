from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, \
    HttpResponseNotAllowed

from models import *


def index(request):
    return HttpResponseRedirect(reverse("login"))


def home(request):
    user = request.user

    if not user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))

    if not user.email or not user.is_active:
        import registrar.views as registrar
        return registrar.user_activation_required(request)

    matches = Match.objects.all().order_by('-date')
    predictions = user.predictions.all()
    pairs=[]
    for match in matches:
        found = False
        for predict in predictions:
            if predict.match_id == match.id:
                pairs.append((match, predict))
                found = True
                break
        if not found:
            pairs.append((match, None))

    scores = Score.objects.all().order_by("-value")

    data = {"pairs": pairs, "scores": scores}
    data.update(Badge.DICT)

    return render(request, "index.html", data)


def submit_prediction(request):
    if not "match_pk" in request.POST or not "home_r" in request.POST or not "away_r" in request.POST:
        return HttpResponseBadRequest("prediction lacks core elements!")

    user = request.user
    match = Match.objects.get(pk=request.POST["match_pk"])

    if match.due or match.finished:
        return HttpResponseNotAllowed("Hey you can't predict a match after it is started!")

    try:
        prediction = user.predictions.get(match=match)
        prediction.home_result = request.POST["home_r"]
        prediction.away_result = request.POST["away_r"]
        prediction.home_penalty = request.POST["home_p"] if "home_p" in request.POST else None
        prediction.away_penalty = request.POST["away_p"] if "away_p" in request.POST else None
        prediction.save()
    except Predict.DoesNotExist:
        prediction = Predict.objects.create(user=user,
                                            match=match,
                                            home_result=request.POST["home_r"],
                                            away_result=request.POST["away_r"],
                                            home_penalty=request.POST["home_p"] if "home_p" in request.POST else None,
                                            away_penalty=request.POST["away_p"] if "away_p" in request.POST else None)
    data = {"match": match, "predict": prediction}
    data.update(Badge.DICT)
    return render(request, 'match_list_item.html', data)
