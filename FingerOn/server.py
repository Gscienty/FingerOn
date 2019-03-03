from gevent.pywsgi import WSGIServer
from . import router
from . import action

class Server(WSGIServer):

    def __application(self, environment, start_response):
        uri = environment['PATH_INFO']
        action = self.router.get(uri)
        if action is None:
            return []

        action_result = action.execute(environment)
        return []

    def __init__(self, sockAddr):
        self.router = router.Router()
        WSGIServer.__init__(self, listener=sockAddr, application=self.__application)

    def __wrapper_action(self, action_type, uri):
        def __wrapper(func):
            act = action.Action(action_type, uri, func)
            self.router.add_action(act)
        return __wrapper

    def restful(self, uri):
        return self.__wrapper_action('restful', uri)

    def graphql(self, uri):
        return self.__wrapper_action('graphql', uri)

    def run(self):
        self.serve_forever()
