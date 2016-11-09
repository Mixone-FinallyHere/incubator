from django.http import JsonResponse
from django.shortcuts import render

from promises.models import Promise, Slot


def timeline(request):
    return JsonResponse({
        'slots': [{
            'start': s.start.timestamp(),
            'stop': s.stop.timestamp(),
        } for s in Slot.objects.all()],
        'promises': [{
            'start': p.start.timestamp(),
            'stop': p.stop.timestamp(),
            'username': p.user.username,
            'user_id': p.user.id,
        } for p in Promise.objects.all()],
    })


def demo(request):
    return render(request, "timeline_demo.html")
