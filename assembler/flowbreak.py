class FlowBreak(Exception):
    """
    Base class for all of our flow break exceptions.
    """
    def __init__(self, label, line_num):
        super().__init__("Flow break")
        self.label = label
        self.line_num = line_num
        self.msg = "Unknown control flow exception."


class Jump(FlowBreak):
    def __init__(self, label, line_num):
        super().__init__(label, line_num)
        self.msg = "Jump to " + label
