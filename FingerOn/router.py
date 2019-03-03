class Router:

    def __init__(self):
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def get(self, env):
        for action in self.actions:
            if action.match(env):
                return action
        return None
