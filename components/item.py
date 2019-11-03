class Item:
    def __init__(self, use_function = None, targeting=False, targeting_message=None, can_stack=False, count=1, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.can_stack = can_stack
        self.count = count
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs