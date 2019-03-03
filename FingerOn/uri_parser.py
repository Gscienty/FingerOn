import re

class URIParser:

    def __init__(self, uri):
        self.originURI = uri
        self.params = []

        self.__analysis(uri)

    def __analysis(self, uri):
        params = re.findall(r'(\{\s*([a-zA-Z_]\w*)\s*:\s*(int|string|real)\s*\})', uri);
        self.reg = '^' + uri + '$'
        for param in params:
            if param[-1] == 'int':
                self.reg = self.reg.replace(param[0], '(\d+)')
            elif param[-1] == 'string':
                self.reg = self.reg.replace(param[0], '(.+)')
            elif param[-1] == 'real':
                self.reg = self.reg.replace(param[0], '(\d*\.\d*|\d*\.?|\.\d*)')
            self.params.append(param)


    def match(self, uri):
        return re.match(self.reg, uri) is not None
        
    def param(self, uri):
        params = re.match(self.reg, uri).groups()
        if len(params) is not len(self.params):
            return None

        def __translate(val, tp):
            if tp == 'string':
                return val
            elif tp == 'int':
                return int(val)
            elif tp == 'real':
                return float(val)
            return None

        return [
                (self.params[i][1], __translate(params[i], self.params[i][-1]))
                for i in range(len(self.params))
        ]
