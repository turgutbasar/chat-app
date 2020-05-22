import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .message_bus import MessageBus

message_bus = MessageBus()


def index(request):
    return render(request, 'index.html')


def room(request):
    user_name = request.GET.get('u', 'default')
    return render(request, 'room.html', {
        'user_name': user_name
    })


def message_send(request):
    if request.method == "POST":
        message = json.loads(request.body)
        if message is not None:
            message_bus.notify(message)
    return HttpResponse()


def message_listener(request):
    if request.method == "GET":
        user_id = request.GET.get('u', None)
        if user_id is not None:
            listener = message_bus.attach(user_id)
            # Wait for 30 secs
            try:
                if listener.signal_condition.wait(30):  # if there is at least one message
                    messages = listener.message_buffer.copy()
                    return JsonResponse({'messages': messages})
                return HttpResponse(status=503)
            finally:
                message_bus.detach(user_id)
    return HttpResponse()

