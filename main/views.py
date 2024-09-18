import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .forms import MoodEntryForm
from .models import MoodEntry
from django.contrib import messages
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been successfully created!")
            return redirect("main:login")
    context = {"form": form}
    return render(request, "register.html", context)


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie("last_login", str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {"form": form}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie("last_login")
    return response


@login_required(login_url="main:login")
def show_main(request: HttpRequest):
    mood_entries = MoodEntry.objects.request(user=request.user)

    context = {
        "name": request.user.username,
        "npm": "2306221900",
        "name": "Thorbert Anson Shi",
        "class": "PBP E",
        "mood_entries": mood_entries,
        "last_login": request.COOKIES["last_login"],
    }

    return render(request, "main.html", context)


def create_mood_entry(request: HttpRequest):
    form = MoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        mood_entry = form.save(commit=False)
        mood_entry.user = request.user
        mood_entry.save()
        return redirect("main:show_main")

    context = {"form": form}
    return render(request, "create-mood-entry.html", context)


def show_xml(request: HttpRequest):
    data = MoodEntry.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data), content_type="application/xml"
    )


def show_json(request: HttpRequest):
    data = MoodEntry.objects.all()
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )


def show_xml_by_id(request: HttpRequest, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("xml", data), content_type="application/xml"
    )


def show_json_by_id(request: HttpRequest, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )
