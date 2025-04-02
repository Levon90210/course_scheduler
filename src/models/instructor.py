from typing import List, Set

class Instructor:
    name: str
    availability: Set[str]
    preferred_courses: Set[str]
    max_hours: int

    def __init__(self, name: str, availability: List[str], preferred_courses: List[str], max_hours: int) -> None:
        self.name = name
        self.availability = set(availability)
        self.preferred_courses = set(preferred_courses)
        self.max_hours = max_hours