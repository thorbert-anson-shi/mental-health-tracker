from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import MoodEntryForm
from .models import MoodEntry
from django.core import serializers


def show_main(request: HttpRequest):
    mood_entries = MoodEntry.objects.all()

    context = {
        "npm": "2306221900",
        "name": "Thorbert Anson Shi",
        "class": "PBP E",
        "mood_entries": mood_entries,
    }

    return render(request, "main.html", context)


def create_mood_entry(request: HttpRequest):
    form = MoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
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
