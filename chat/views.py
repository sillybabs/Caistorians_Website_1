from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import GroupChatRoom, GroupMessage

@login_required
def redirect_to_chat(request):
    """Redirect user to their cohort chat"""
    print("Entered redirect_to_chat")
    print("User:", request.user.username)

    year = getattr(request.user, 'graduation_year', None)
    print("Graduation year:", year)

    if not year:
        print("No graduation year — rendering error page.")
        return render(request, 'chat/error.html', {'message': 'Graduation year not set.'})

    print(f"Redirecting to chat: cohort year {year}")
    return redirect('chat:cohort_chat', cohort_year=year)


@login_required
def cohort_chat_view(request, cohort_year):
    """Render chat page for a given cohort"""
    print("Entered cohort_chat_view")
    print("Cohort year from URL:", cohort_year)
    print("User:", request.user.username)

    room, created = GroupChatRoom.objects.get_or_create(cohort_year=cohort_year)
    print("Room fetched/created:", room)
    print("Room newly created:", created)

    messages = GroupMessage.objects.filter(room=room)
    print("Number of messages:", messages.count())

    print("Rendering cohort_chat.html now")
    return render(request, 'chat/cohort_chat.html', {
        'room': room,
        'messages': messages,
    })
