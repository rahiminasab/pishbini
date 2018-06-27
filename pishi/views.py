from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from models import *
from match.forms import SoccerMatchPredictionForm


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
                if match.due:
                    pairs.append((match, predict, None))
                else:
                    pairs.append((match, predict, SoccerMatchPredictionForm(instance=predict)))
                found = True
                break
        if not found:
            if match.due:
                pairs.append((match, None, None))
            else:
                pairs.append((match, None, SoccerMatchPredictionForm()))

    scores = Score.objects.all().order_by("-value")

    data = {"pairs": pairs, "scores": scores}
    data.update(Badge.DICT)

    return render(request, "index.html", data)
