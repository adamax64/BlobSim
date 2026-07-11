class NoGrandmasterFoundException(Exception):
    """Exception raised when no current grandmaster is found in the system."""

    def __init__(self, message: str = "No current grandmaster found"):
        self.message = message
        super().__init__(self.message)
