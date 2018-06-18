from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotAllowed

from models import *
from forms import SignUpForm


def index(request):
    return HttpResponseRedirect(reverse("login"))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    user = request.user

    if not user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))

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

    return render(request, "index.html", {"pairs": pairs})


def submit_prediction(request):
    if not "match_pk" in request.POST or not "home_r" in request.POST or not "away_r" in request.POST:
        return HttpResponseBadRequest("prediction lacks core elements!")

    user = request.user
    match = Match.objects.get(pk=request.POST["match_pk"])

    if match.due:
        return HttpResponseNotAllowed("Hey you can't predict a match after it is started")

    predict = Predict.objects.create(user=user,
                                     match=match,
                                     home_result_predict=request.POST["home_r"],
                                     away_result_predict=request.POST["away_r"],
                                     home_penalty_predict=request.POST["home_p"] if "home_p" in request.POST else None,
                                     away_penalty_predict=request.POST["away_p"] if "away_p" in request.POST else None)

    data = {"match": match, "predict": predict}
    return render(request, 'match.html', data)
