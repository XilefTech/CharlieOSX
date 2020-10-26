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

        @self.app.route("/api")
        def api(req, resp):
            yield from picoweb.start_response(resp, content_type = "text/html")
            
            proc = req.qs.split("&")
            self.outDict = {}
            for elm in proc:
                temp = elm.split("=")
                try:
                    self.outDict[temp[0]] = int(temp[1])
                except:
                    self.outDict[temp[0]] = temp[1]

    def startServerThread(self):
        def runWebserver():
            with self.weblock:
                self.app.run(debug = -1, host = '192.168.178.52')
        _thread.start_new_thread(runWebserver, ())

    def getResponseData(self):
        return self.outDict


