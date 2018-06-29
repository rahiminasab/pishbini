from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, \
    HttpResponseNotAllowed
from django.views.decorators.http import require_POST

from copy import copy

from .forms import SoccerMatchPredictionForm
from ..models import MatchSet, Match, Badge, Predict, Score


def render_matches(request, match_set_id):
    try:
        match_set = MatchSet.objects.get(id=MatchSet.decode_id(match_set_id))
    except MatchSet.DoesNotExist:
        return HttpResponseBadRequest("No MatchSet found with requested id=%s" % match_set_id)

    user = request.user
    matches = match_set.matches.all().order_by('-date')
    predictions = {predict.match.id: predict for predict in user.predictions.all()}
    pairs = []
    for match in matches:
        prediction = predictions.get(match.id)
        if match.due:
            pairs.append((match, prediction, None))
        else:
            pairs.append((match, prediction, SoccerMatchPredictionForm(instance=prediction)))

    scores = match_set.scores.all().order_by("-value")

    data = {"match_set": match_set, "pairs": pairs, "scores": scores}
    data.update(Badge.index_dict)

    return render(request, 'match/match_set_expand.html', data)



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
    data.update(Badge.index_dict)
    return render(request, 'match/soccer/match_list_item.html', data)
