class NoCurrentEventException(Exception):
    """Exception raised when there is no current event."""
    def __init__(self, message="No event today according to calendar."):
        self.message = message
        super().__init__(self.message)
