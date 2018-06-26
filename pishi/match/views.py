from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, \
    HttpResponseNotAllowed

from .forms import SoccerMatchPredictionForm
from ..models import Match, Badge, Predict


def submit_prediction(request):
    if request.method == "POST":
        form = SoccerMatchPredictionForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = SoccerMatchPredictionForm()
    data = {"match": match, "predict": prediction, "form": form}
    data.update(Badge.DICT)
    return render(request, 'match/soccer/match_list_item.html', data)

    if not "match_pk" in request.POST or not "home_r" in request.POST or not "away_r" in request.POST:
        return HttpResponseBadRequest("prediction lacks core elements!")

    user = request.user
    match = Match.objects.get(pk=request.POST["match_pk"])

    if match.due or match.finished:
        return HttpResponseNotAllowed("Hey you can't predict a match after it is started!")

    try:
        prediction = user.predictions.get(match=match)
        prediction.home_result_predict = request.POST["home_r"]
        prediction.away_result_predict = request.POST["away_r"]
        prediction.home_penalty_predict = request.POST["home_p"] if "home_p" in request.POST else None
        prediction.away_penalty_predict = request.POST["away_p"] if "away_p" in request.POST else None
        prediction.save()
    except Predict.DoesNotExist:
        prediction = Predict.objects.create(user=user,
                                            match=match,
                                            home_result_predict=request.POST["home_r"],
                                            away_result_predict=request.POST["away_r"],
                                            home_penalty_predict=request.POST["home_p"] if "home_p" in request.POST else None,
                                            away_penalty_predict=request.POST["away_p"] if "away_p" in request.POST else None)
    data = {"match": match, "predict": prediction}
    data.update(Badge.DICT)
    return render(request, 'match/soccer/match_list_item.html', data)
