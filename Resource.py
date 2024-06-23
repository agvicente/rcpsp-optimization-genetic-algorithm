class Resource:
    def __init__(
            self, 
            name: str, 
            per_period_availability: int
    ) -> None:
        self.name = name
        self.per_period_availability = per_period_availability