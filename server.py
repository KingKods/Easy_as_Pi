import tornado.ioloop
import tornado.web
import tornado.websocket
import webbrowser

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("FrontEnd.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    latCordList = []
    lngCordList = []


    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}

    def on_message(self, message):        
        
        #when we receive some message we want some message handler..
        #for this example i will just print message to console
        print("Client %s received a message : %s" % (self.id, message))
        number_string = message.split(',')
        number_string = [float(i) for i in number_string]
        print('The Message has been convert to the following array: ' + number_string)



    def on_close(self):
        if self.id in clients:
            del clients[self.id]

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', WebSocketHandler),
])

if __name__ == '__main__':
    tornado.ioloop.IOLoop.instance().start()
