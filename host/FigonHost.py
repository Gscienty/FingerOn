from gevent.pywsgi import WSGIServer

class FigonHost(WSGIServer):

    def __application(self, environment, start_response):
        if self.app is None:
            return []
        else:
            return self.app(environment, start_response)

    def __init__(self, sockAddr):
        WSGIServer.__init__(self, listener=sockAddr, application=self.__application)

    def setApplication(self, app):
        self.app = app

    def run(self):
        self.serve_forever()
