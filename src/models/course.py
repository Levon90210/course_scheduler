from typing import List

class Course:
    name: str
    times_per_week: int
    preferred_time_slots: List[str]

    def __init__(self, name: str, times_per_week: int, preferred_time_slots: List[str]) -> None:
        self.name = name
        self.times_per_week = times_per_week
        self.preferred_time_slots = preferred_time_slots