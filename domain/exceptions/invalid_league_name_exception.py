class InvalidLeagueNameException(Exception):
    """Exception raised when league names are missing or empty."""

    def __init__(self, message="League names in English and Hungarian are required."):
        self.message = message
        super().__init__(self.message)
