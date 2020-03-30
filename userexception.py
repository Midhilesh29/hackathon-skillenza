class NoSolution(Exception):
    def __init__(self, arg):
        self.args = arg