from gevent.pywsgi import WSGIServer
from . import router
from . import action

class Server(WSGIServer):

    def __application(self, env, start_response):
        action = self.router.get(env)
        if action is None:
            return []

        action_result = action.execute(env)
        return []

    def __init__(self, sockAddr):
        self.router = router.Router()
        WSGIServer.__init__(self, listener=sockAddr, application=self.__application)

    def __wrapper_action(self, action_type, uri, **kwargs):
        def __wrapper(func):
            act = action.Action(action_type, uri, func, **kwargs)
            self.router.add_action(act)
        return __wrapper

    def restful(self, uri, **kwargs):
        return self.__wrapper_action('restful', uri, **kwargs)

    def graphql(self, uri, **kwargs):
        return self.__wrapper_action('graphql', uri, **kwargs)

    def run(self):
        self.serve_forever()
