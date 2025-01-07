class NameOccupiedException(Exception):
    def __init__(self, message="This name is already taken! Give a different name"):
        self.message = message
        super().__init__(self.message)
