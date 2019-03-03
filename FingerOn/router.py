class Router:

    def __init__(self):
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def get(self, uri):
        for action in self.actions:
            if action.match(uri):
                return action
        return None
