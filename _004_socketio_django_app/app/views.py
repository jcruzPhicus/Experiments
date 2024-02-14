from django.shortcuts import render
from django.conf import settings
import socketio

# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed

if settings.SERVER_TYPE == "ASGI":
    sio = socketio.AsyncServer(async_mode="asgi")
else:
    sio = socketio.Server(async_mode=None)
# Create your views here.


def index(request):
    return render(request, "index.html")


@sio.event
def send_message(sid, message):
    print(f"Called send_message with {message}")

    sio.emit("message", {
             "username": message["username"], 'data': message['data']}, room=message["room"])


@sio.event
def join(sid, message):
    print(f"Called join with message {message}")
    sio.enter_room(sid, message['room'])
    sio.emit("join_response", {'room': message['room'], "username": message["username"]},
             room=sid)


@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit("leave_response", {'room': message['room'], "username": message["username"]},
             room=sid)


@sio.event
def connect(sid, environ):
    print("Client connected")


@sio.event
def disconnect(sid):
    print('Client disconnected')
