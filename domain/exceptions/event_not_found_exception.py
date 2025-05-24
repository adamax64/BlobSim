class EventNotFoundException(Exception):
    """Exception raised when there is no event found."""
    def __init__(self, message="No event found for specified id."):
        self.message = message
        super().__init__(self.message)
