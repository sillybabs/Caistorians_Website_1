# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, RSVP
from .forms import EventForm, RSVPForm
from django.contrib import messages






def event_list_view(request):
    events = Event.objects.order_by("start_time")
    return render(request, "events/event_list.html", {"events": events})


def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    rsvps = event.rsvps.select_related("user")

    user_status = None
    if request.user.is_authenticated:
        try:
            user_status = RSVP.objects.get(event=event, user=request.user).status
        except RSVP.DoesNotExist:
            pass
    
    rsvps_yes = event.rsvps.filter(status="yes").count()
    rsvps_maybe = event.rsvps.filter(status="maybe").count()
    rsvps_no = event.rsvps.filter(status="no").count()
    
    return render(request, "events/event_detail.html", {
        "event": event,
        "rsvps_yes": rsvps_yes,
        "rsvps_maybe": rsvps_maybe,
        "rsvps_no": rsvps_no,
    })



@login_required
def rsvp_view(request, pk, status):
    event = get_object_or_404(Event, pk=pk)
    RSVP.objects.update_or_create(
        event=event, user=request.user, defaults={"status": status}
    )
    return redirect("events:event_detail", pk=pk)


@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect("events:event_list")
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form})

# events/views.py
from django.http import HttpResponseForbidden

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.created_by != request.user:
        return HttpResponseForbidden("You cannot edit this event.")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("events:event_detail", pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, "events/event_form.html", {"form": form})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.created_by != request.user:  # permission check
        return HttpResponseForbidden("You cannot delete this event.")

    if request.method == "POST":
        event.delete()
        return redirect("events:event_list")
    return render(request, "events/event_confirm_delete.html", {"event": event})


# events/views.py
@login_required
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    try:
        rsvp = RSVP.objects.get(event=event, user=request.user)
    except RSVP.DoesNotExist:
        rsvp = None

    if request.method == "POST":
        form = RSVPForm(request.POST, instance=rsvp)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.user = request.user
            rsvp.event = event
            rsvp.save()
            messages.success(request, "Your RSVP has been saved.")
            return redirect("events:event_detail", pk=event.pk)
    else:
        form = RSVPForm(instance=rsvp)

    return render(request, "events/rsvp_form.html", {"form": form, "event": event})
