from src.scheduler import *

def load_instructors(data):
    return [Instructor(instructor['name'],
                       instructor['availability'],
                       instructor['preferred_courses'],
                       instructor['max_hours'])
            for instructor in data['instructors']]

def load_courses(data):
    return [Course(course['name'],
                   course['times_per_week'],
                   course['preferred_time_slots'],)
            for course in data['courses']]

def load_scheduler(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

        instructors = load_instructors(data)
        courses = load_courses(data)
        time_slots = data['time_slots']

        return Scheduler(courses, instructors, time_slots)