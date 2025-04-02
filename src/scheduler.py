from pulp import *
from typing import List, Dict, Tuple, TypedDict
from src.models import *
from src.utils.schedule_utils import *
from src.utils.timeslot_utils import *

class ScheduleEntry(TypedDict):
    """Type definition for scheduled items"""
    time_slot: str
    course: str
    instructor: str

class Scheduler:
    """Main scheduler class that generates the schedule"""
    schedule: List[Tuple[str, str, str]]

    def __init__(self,
                 courses: List[Course],
                 instructors: List[Instructor],
                 time_slots: List[str]) -> None:
        self.courses = courses
        self.time_slots = time_slots
        self.instructors = instructors
        self.schedule = []

    def solve(self) -> str:
        """Solve the course scheduling problem using linear programming"""
        prob = LpProblem("Course_Scheduling", LpMinimize)

        x: Dict[Tuple[str, str, str], LpVariable] = LpVariable.dicts(
            "schedule",
            [(c.name, t, i.name)
            for c in self.courses
            for t in self.time_slots
            for i in self.instructors],
            cat='Binary'
        )

        # 1. Each course must be scheduled required times per week
        for c in self.courses:
            prob += lpSum(x[(c.name, t, i.name)]
                          for t in self.time_slots
                          for i in self.instructors) == c.times_per_week

        # 2. Only one course at a time slot
        for t in self.time_slots:
            prob += lpSum(x[(c.name, t, i.name)]
                          for c in self.courses
                          for i in self.instructors) <= 1

        # 3. Instructor must be available
        for i in self.instructors:
            for t in self.time_slots:
                if t not in i.availability:
                    for c in self.courses:
                        prob += x[(c.name, t, i.name)] == 0

        # 4. Instructor workload must not exceed the limit
        for i in self.instructors:
            prob += lpSum(get_time_slot_length(t) * x[(c.name, t, i.name)]
                          for c in self.courses
                          for t in self.time_slots) <= i.max_hours

        # 5. Course must be preferred by an instructor
        for i in self.instructors:
            for c in self.courses:
                if c.name not in i.preferred_courses:
                    for t in self.time_slots:
                        prob += x[(c.name, t, i.name)] == 0

        # Objective function
        prob += lpSum(x[(c.name, t, i.name)] * (
            (0 if t in c.preferred_time_slots else 1) # Time slot preference penalty
            + get_time_penalty(t) # Late day penalty
        )
                      for c in self.courses
                      for t in self.time_slots
                      for i in self.instructors)

        prob.solve()

        if LpStatus[prob.status] == "Optimal":
            self.schedule = [
                (c.name, t, i.name)
                for c in self.courses
                for t in self.time_slots
                for i in self.instructors
                if x[(c.name, t, i.name)].value() == 1
            ]
        return LpStatus[prob.status]

    def get_output_data(self) -> List[ScheduleEntry]:
        """Convert the schedule to a list of ScheduleEntry objects"""
        data: List[ScheduleEntry] = []
        for c, t, i in self.schedule:
            data.append({
                "time_slot": t,
                "course": c,
                "instructor": i
            })
        return data

    def save_schedule(self, filename: str = "data/output.json") -> None:
        """Save the schedule to JSON"""
        schedule_data = self.get_output_data()
        save_schedule(schedule_data, filename)

    def print_schedule(self) -> None:
        """Print the schedule as a table"""
        schedule_data = self.get_output_data()
        print_schedule_table(schedule_data)