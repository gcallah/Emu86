class FlowBreak(Exception):
    """
    Base class for all of our flow break exceptions.
    """
    def __init__(self, label):
        super().__init__("Flow break")
        self.label = label
        self.msg = "Unknown control flow exception."


class Jump(FlowBreak):
    def __init__(self, label):
        super().__init__(label)
        self.msg = "Jump to " + label
