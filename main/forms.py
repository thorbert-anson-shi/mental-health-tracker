from django.forms import ModelForm
from .models import MoodEntry


class MoodEntryForm(ModelForm):
    class Meta:
        model = MoodEntry
        fields = ["mood", "feelings", "mood_intensity"]
