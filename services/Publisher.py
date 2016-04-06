import redis
from functools import partial
from tornado import websocket, web, ioloop
import threading
LISTENERS = []

def redis_listener():
    client = redis.StrictRedis(host='localhost', port=6379, db=0)
    ps = client.pubsub()
    ps.subscribe('first_channel')
    io_loop = ioloop.IOLoop.instance()
    for message in ps.listen():
        for element in LISTENERS:
            io_loop.add_callback(partial(element.on_message, message))

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")


class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        LISTENERS.append(self)

    def on_message(self, item):

        try:
            message = unicode(item['data'])
            self.write_message(message)
            print ("Message sent")
        except:
            print ("No valid message")
            pass

    def on_close(self):
        print("WebSocket closed")


app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', EchoWebSocket),
])

if __name__ == '__main__':
    threading.Thread(target=redis_listener).start()
    app.listen(8888)
    ioloop.IOLoop.instance().start()
