from src.scheduler import Scheduler
from src.models import *
import sys
from typing import Dict, List
import re
import json

def validate_inputs(data: Dict) -> List[str]:
    errors = []

    top_level_structure = {"courses", "instructors", "time_slots"}
    if not top_level_structure.issubset(data.keys()):
        errors.append(f"Missing keys: {top_level_structure - set(data.keys())}")
        return errors

    time_slots = set(data["time_slots"])
    for slot in time_slots:
        if not isinstance(slot, str):
            errors.append(f"Time slot '{slot}' is not a string")
            continue
        pattern = r"^[A-Za-z]+\s(09|1[0-9]|2[0-3]):([0-5][0-9])-(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$"
        if not re.match(pattern, slot):
            errors.append(f"Invalid time slot format: '{slot}'. Expected 'Day HH:MM-HH:MM'")

    course_structure = {"name", "times_per_week", "preferred_time_slots"}
    for course in data["courses"]:
        if not course_structure.issubset(course.keys()):
            errors.append(f"Missing course keys: {course_structure - set(course.keys())}")

    instructor_structure = {"name", "availability", "preferred_courses", "max_hours"}
    for instructor in data["instructors"]:
        if not instructor_structure.issubset(instructor.keys()):
            errors.append(f"Missing instructor keys: {instructor_structure - set(instructor.keys())}")

    return errors


def load_instructors(data: Dict) -> List[Instructor]:
    return [Instructor(instructor['name'],
                       instructor['availability'],
                       instructor['preferred_courses'],
                       instructor['max_hours'])
            for instructor in data['instructors']]

def load_courses(data: Dict) -> List[Course]:
    return [Course(course['name'],
                   course['times_per_week'],
                   course['preferred_time_slots'],)
            for course in data['courses']]

def load_scheduler(file_path: str) -> Scheduler:
    with open(file_path, 'r') as f:
        data = json.load(f)

        validation_errors = validate_inputs(data)
        if len(validation_errors) > 0:
            print("Invalid input file!")
            for error in validation_errors:
                print(error)
            sys.exit(1)
        else:
            instructors = load_instructors(data)
            courses = load_courses(data)
            time_slots = data['time_slots']

        return Scheduler(courses, instructors, time_slots)
