from pulp import *


class Instructor:
    def __init__(self, name, availability, preferred_courses, max_hours):
        self.name = name
        self.availability = set(availability)
        self.preferred_courses = set(preferred_courses)
        self.max_hours = max_hours


class Course:
    def __init__(self, name, times_per_week, preferred_time_slots):
        self.name = name
        self.times_per_week = times_per_week
        self.preferred_time_slots = preferred_time_slots


class Scheduler:
    def __init__(self, courses, instructors, time_slots):
        self.courses = courses
        self.time_slots = time_slots
        self.instructors = instructors
        self.prob = None

    def solve(self):
        prob = LpProblem("Course_Scheduling", LpMinimize)

        x = LpVariable.dicts("schedule",
                             [(c.name, t, i.name)
                              for c in self.courses
                              for t in self.time_slots
                              for i in self.instructors],
                             cat='Binary')

        for c in self.courses:
            prob += lpSum(x[(c.name, t, i.name)]
                          for t in self.time_slots
                          for i in self.instructors) == c.times_per_week

        for t in self.time_slots:
            prob += lpSum(x[(c.name, t, i.name)]
                          for c in self.courses
                          for i in self.instructors) <= 1

        for i in self.instructors:
            for t in self.time_slots:
                if t not in i.availability:
                    for c in self.courses:
                        prob += x[(c.name, t, i.name)] == 0

        for i in self.instructors:
            for t in self.time_slots:
                prob += lpSum(x[(c.name, t, i.name)]
                              for c in self.courses) <= 1

        for i in self.instructors:
            prob += lpSum(1.5 * x[(c.name, t, i.name)]
                          for c in self.courses
                          for t in self.time_slots) <= i.max_hours

        for i in self.instructors:
            for c in self.courses:
                if c.name not in i.preferred_courses:
                    for t in self.time_slots:
                        prob += x[(c.name, t, i.name)] == 0

        prob += lpSum(x[(c.name, t, i.name)] * (0 if t in c.preferred_time_slots else 1)
                      for c in self.courses
                      for t in self.time_slots
                      for i in self.instructors), "Minimize_non_preferred_times"

        prob.solve()

        print("Status:", LpStatus[prob.status])
        if LpStatus[prob.status] == "Optimal":
            print("\nOptimal Schedule:")
            for c in self.courses:
                for t in self.time_slots:
                    for i in self.instructors:
                        if x[(c.name, t, i.name)].value() == 1:
                            print(
                                f"{c.name:10} at {t:10} with {i.name:15} (Preferred: {'yes' if t in c.preferred_time_slots else 'no'})")
            print("\nInstructor Workload:")
            for i in self.instructors:
                hours = sum(1.5 * x[(c.name, t, i.name)].value()
                            for c in self.courses
                            for t in self.time_slots)
                print(f"{i.name:15}: {hours} hours (max {i.max_hours})")
        else:
            print("No feasible solution found.")
            if LpStatus[prob.status] == "Infeasible":
                print("\nTry relaxing some constraints (e.g., instructor preferences or max hours)")