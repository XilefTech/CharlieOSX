import picoweb, _thread


class Webremote():
    '''docstring'''

    def __init__(self):
        self.app = picoweb.WebApp("app")
        self.outDict = {}
        self.weblock = _thread.allocate_lock()

        @self.app.route("/")
        def index(req, resp):
            yield from picoweb.start_response(resp, content_type = "text/html")
        
            htmlFile = open('site.html', 'r')
        
            for line in htmlFile:
                yield from resp.awrite(line)
    def startServerThread(self):
        def runWebserver():
            with self.weblock:
                self.app.run(debug = -1, host = '192.168.178.52')
        _thread.start_new_thread(runWebserver, ())

