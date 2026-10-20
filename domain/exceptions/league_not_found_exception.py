class LeagueNotFoundException(Exception):
    """Exception raised when a league cannot be found by id."""

    def __init__(self, league_id: int):
        self.league_id = league_id
        self.message = f"League not found for id {league_id}."
        super().__init__(self.message)
