import random

class GreedyGridAgent:
    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']
    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """Pure condition-action rules — no memory."""
    def sense_and_act(self, percept: dict) -> str:
        if percept.get('wall_ahead'):
            return 'Left'          # IF wall_ahead THEN turn_left
        if percept.get('food_here'):
            return 'Up'            # IF food_here THEN act
        return 'Up'                # ELSE move_forward


class ModelBasedAgent:
    """Keeps internal state so it doesn't repeat a failed action."""
    def __init__(self):
        self.last_action = None

    def sense_and_act(self, percept: dict) -> str:
        options = ['Left', 'Right', 'Down', 'Up']
        if percept.get('wall_ahead'):
            if self.last_action in options:
                idx = options.index(self.last_action)
                action = options[(idx + 1) % len(options)]   # rotate to a NEW action
            else:
                action = options[0]
        elif percept.get('food_here'):
            action = 'Up'
        else:
            action = 'Up'
        self.last_action = action
        return action

class SearchAgent:
    """Placeholder for Lab 3 Search Agent."""
    def __init__(self):
        pass

    def sense_and_act(self, percept: dict) -> str:
        return 'Up'