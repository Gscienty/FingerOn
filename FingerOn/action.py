from . import uri_parser

class Action:

    def __init__(self, action_type, uri, func, **kwargs):
        self.action_param_type = action_type
        self.func = func
        self.uri = uri_parser.URIParser(uri)
        if 'methods' in kwargs:
            self.methods = kwargs['methods']
        else:
            self.methods = [ 'GET', 'POST', 'PUT', 'DELETE' ]

    def action_type(self):
        return self.action_param_type

    def action(self):
        return self.func

    def match(self, env):
        return self.uri.match(env['PATH_INFO']) and env['REQUEST_METHOD'] in self.methods

    def __uri_param(self, uri):
        return self.uri.param(uri)

    def __restful_execute(self, env):
        uri_params = self.__uri_param(env['PATH_INFO'])

        dict_args = {}
        for param in uri_params:
            dict_args[param[0]] = param[1]
        # TODO add body
        print(env)

        return self.func(**dict_args)

    def __graphql_execute(self, env):
        # TODO add ctx & schema & others
        dict_args = {}
        for param in uri_params:
            dict_args[param[0]] = param[1]

        return self.func(**dict_args)

    def execute(self, env):
        ret = None
        if self.action_param_type == 'restful':
            ret = self.__restful_execute(env)
        elif self.action_param_type == 'graphql':
            ret = self.__graphql_execute(env)
        return ret

