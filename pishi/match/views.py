from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, \
    HttpResponseNotAllowed
from django.views.decorators.http import require_POST

from copy import copy

from .forms import SoccerMatchPredictionForm
from ..models import Match, Badge, Predict


@require_POST
def submit_prediction(request, match_id):
    try:
        match = Match.objects.get(pk=Match.decode_id(match_id))
    except Match.DoesNotExist:
        return HttpResponseBadRequest("No Match found with requested id=%s"%match_id)

    user = request.user

    try:
        prediction = user.predictions.get(match=match)
    except Predict.DoesNotExist:
        prediction = Predict(match=match, user=user)

    init_prediction = copy(prediction)

    form = SoccerMatchPredictionForm(request.POST, instance=prediction, match=match)

    if form.is_valid():
        prediction.save()
    else:
        prediction = init_prediction

    data = {"match": match, "predict": prediction, "form": form}
    data.update(Badge.DICT)
    return render(request, 'match/soccer/match_list_item.html', data)
