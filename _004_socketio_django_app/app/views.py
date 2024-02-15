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


thread = None


def index(request):
    return render(request, "index.html")


def background_heartbeat():
    while True:
        sio.send("hii", room="heartbeat")
        sio.sleep(5)


@sio.event
def query(sid):
    sio.send(sio.rooms(sid), to=sid)


@sio.event
def subscribe(sid, message):
    print(f"Called join with message {message}")
    sio.enter_room(sid, message['room'])
    sio.emit("subscription_response", {'room': message['room'], "username": message["username"]},
             room=sid)


@sio.event
def unsubscribe(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit("unsubscription_response", {'room': message['room'], "username": message["username"]},
             room=sid)


@sio.event
def start_heartbeat(sid, message):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_heartbeat)


@sio.event
def stop_heartbeat(sid, message):
    global thread
    if thread is not None:
        thread.cancel()
        del thread
        thread = None


@sio.event
def connect(sid, environ):
    print("Client connected")


@sio.event
def disconnect(sid):
    print('Client disconnected')
