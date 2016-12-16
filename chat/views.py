from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from chat.models import Room


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user=user)
            return HttpResponseRedirect(request.GET.get('next') or reverse('profile'))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid credentials')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


@login_required(login_url=reverse_lazy('user_login'))
def profile(request):
    return render(request, 'profile.html', {
        'user': request.user,
        'rooms': Room.objects.filter()
    })


@login_required(login_url=reverse_lazy('user_login'))
def chat(request, room):
    try:
        chat_room = Room.objects.filter(id=room)[0]
    except IndexError:
        chat_room = None

    chat_history = chat_room.history.order_by('datetime')[:50] if chat_room is not None else []

    return render(request, 'chat.html', {
        'room': chat_room,
        'history': chat_history
    })


@login_required(login_url=reverse_lazy('user_login'))
def history(request, room):
    try:
        chat_room = Room.objects.filter(id=room)[0]
    except IndexError:
        chat_room = None

    chat_history = chat_room.history.order_by('datetime') if chat_room is not None else []

    return render(request, 'history.html', {
        'room': chat_room,
        'history': chat_history
    })
