from django.shortcuts import render, redirect
import random
from time import localtime, strftime

def index(request):
    if "log" not in request.session:
        request.session["log"] = []
    if "gold" not in request.session:
        request.session["gold"] = 0
    return render(request, "index.html")

def process_money(request):
    location = request.POST["location"]
    time = strftime("%x %X", localtime())
    if location == "farm":
        gain = random.randint(10,20)
        request.session["log"].insert(0, f"Sold Wilbur for {gain} gold! {time}")
    elif location == "cave":
        gain = random.randint(5,10)
        request.session["log"].insert(0, f"Mined {gain} gold worth of ore! {time}")
    elif location == "house":
        gain = random.randint(2,5)
        request.session["log"].insert(0, f"Found {gain} gold in the couch cushions! {time}")
    else:
        if request.session["gold"] > 0:
            bet = random.randint(1, min(50, request.session["gold"]))
            result = random.randint(0,1)
            if result == 0:
                event = "Lost"
                gain = -1*bet
            else:
                event = "Won"
                gain = bet
            request.session["log"].insert(0, f"{event} {bet} gold on the ponies! {time}")
        else:
            gain = 0
            request.session["log"].insert(0, f"Nothing to bet! {time}")

    request.session["gold"] += gain
    request.session.modified = True
    return redirect('/')

def reset(request):
    del request.session["gold"]
    del request.session["log"]
    return redirect('/')


