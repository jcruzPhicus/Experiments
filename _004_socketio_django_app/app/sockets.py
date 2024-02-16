from django.conf import settings
import socketio
import jwt

# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
if settings.SERVER_TYPE == "ASGI":
    mgr = socketio.AsyncRedisManager('redis://')
    sio = socketio.AsyncServer(async_mode="asgi", client_manager=mgr)
    namespace_handler = socketio.AsyncNamespace
else:
    mgr = socketio.RedisManager('redis://')
    sio = socketio.Server(async_mode=None, client_manager=mgr,
                          logger=True, engineio_logger=True)
    namespace_handler = socketio.Namespace


class SubscriptionNamespace(namespace_handler):
    def on_query(self, sid, message):
        self.send(data=sio.rooms(sid), to=sid)

    def on_subscribe(self, sid, message):
        print(f"Called join with message {message}")
        self.enter_room(sid, message['room'])
        self.send(data={'room': message['room']}, to=sid)

    def on_unsubscribe(self, sid, message):
        self.leave_room(sid, message['room'])
        self.send({'room': message['room']},
                  to=sid)


class HeartbeatNamespace(socketio.Namespace):
    thread = None

    def on_start_heartbeat(self, sid, message=None):
        self.enter_room(sid, "heartbeat")
        """         if self.thread is None:
            self.thread = sio.start_background_task(self.background_heartbeat) """

    def on_stop_heartbeat(self, sid, message=None):
        self.leave_room(sid, "heartbeat")
        """         if self.thread is not None:
            self.thread.cancel()
            del self.thread
            self.thread = None """

    def background_heartbeat(self):
        while True:
            self.send("hii", room="heartbeat")
            sio.sleep(5)

    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        self.on_stop_heartbeat(sid)


sio.register_namespace(SubscriptionNamespace("/subscription"))
sio.register_namespace(HeartbeatNamespace("/heartbeat"))
