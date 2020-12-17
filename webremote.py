import picoweb, _thread, time


class Webremote():
    '''docstring'''

    def __init__(self, config, robot, brick):
        self.__config = config
        self.robot = robot
        self.brick = brick
        self.app = picoweb.WebApp("app")
        self.outDict = {'x': 0, 'y': 0, 'a1': 0, 'maxSpeed': 100}
        self.weblock = _thread.allocate_lock()
        self.newData = True

        @self.app.route("/")
        def index(req, resp):
            yield from picoweb.start_response(resp, content_type = "text/html")
        
            htmlFile = open('site/site.html', 'r')
        
            for line in htmlFile:
                yield from resp.awrite(line)

        @self.app.route("/api")
        def api(req, resp):
            yield from picoweb.start_response(resp, content_type = "text/html")
            
            proc = req.qs.split("&")
            for elm in proc:
                temp = elm.split("=")
                try:
                    self.outDict[temp[0]] = int(temp[1])
                except:
                    self.outDict[temp[0]] = temp[1]
            self.newData = True
        
        @self.app.route("/style.css")
        def style(req, resp):
            yield from picoweb.start_response(resp, content_type = "text/css")
            
            htmlFile = open('site/style.css', 'r')
        
            for line in htmlFile:
                yield from resp.awrite(line)

    def run(self):
        self.startServerThread()

        while not any(self.brick.buttons.pressed()):
            if self.newDataAvailable():
                data = self.getResponseData()
                self.robot.setRemoteValues(data)
                #print(data)
            time.sleep(0.05)

    def startServerThread(self):
        def runWebserver():
            with self.weblock:
                self.app.run(debug = -1, host = self.__config['localIP'])
        _thread.start_new_thread(runWebserver, ())

    def getResponseData(self):
        return self.outDict

    def newDataAvailable(self):
        if self.newData:
            self.newData = False
            return True
        else:
            return False


