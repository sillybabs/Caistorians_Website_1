from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Photo, Story
from .forms import PhotoUploadForm, StoryForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden


# --- Photos ---
@login_required
def upload_photo(request):
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            photo.save()
            return redirect("community:gallery")
    else:
        form = PhotoUploadForm()
    return render(request, "community/upload_photo.html", {"form": form})

def gallery_view(request):
    #photos = Photo.objects.filter(approved=True).order_by("-uploaded_at")
    photos = Photo.objects.order_by("-uploaded_at")
    return render(request, "community/gallery.html", {"photos": photos})


# --- Delete Photo ---
@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user != photo.uploaded_by and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this photo.")
    if request.method == "POST":
        photo.delete()
        return redirect("community:gallery")
    return render(request, "community/confirm_delete.html", {"object": photo, "type": "photo"})

# --- Delete Story ---
@login_required
def delete_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.user != story.author and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this story.")
    if request.method == "POST":
        story.delete()
        return redirect("community:story_list")
    return render(request, "community/confirm_delete.html", {"object": story, "type": "story"})

# --- Stories ---
@login_required
def submit_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect("community:story_list")
    else:
        form = StoryForm()
    return render(request, "community/submit_story.html", {"form": form})

def story_list(request):
    #stories = Story.objects.filter(approved=True).order_by("-created_at")
    stories = Story.objects.order_by("-created_at")
    return render(request, "community/story_list.html", {"stories": stories})

def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk, approved=True)
    return render(request, "community/story_detail.html", {"story": story})
