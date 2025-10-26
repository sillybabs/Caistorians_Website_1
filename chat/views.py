
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, MessageeToGroup

@login_required
def year_group_chat(request):
    year_group = request.user.graduation_year
    if not year_group:
        return render(request, 'chat/error.html', {
            'message': 'Your graduation year is not set. Please update your profile.'
        })

    room, _ = ChatRoom.objects.get_or_create(year_group=year_group)
    messages = MessageeToGroup.objects.filter(room=room)

    return render(request, 'chat/year_group_chat.html', {
        'room': room,
        'messages': messages,
    })


from django.shortcuts import redirect

@login_required
def redirect_chat(request):
    if request.user.graduation_year:
        return redirect('chat:year_group_chat', year_group=request.user.graduation_year)
    return render(request, 'chat/error.html', {'message': 'No graduation year set.'})
