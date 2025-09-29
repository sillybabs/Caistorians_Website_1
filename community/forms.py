from django import forms
from .models import Photo, Story

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "caption"]

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["title", "content"]
