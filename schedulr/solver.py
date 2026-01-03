from schedulr.constraints import sections_overlap
from enum import Enum

class Faculty(Enum):
    KSAS = "ksas"
    EN = "engineering"

class ScheduleConstraints:
    """Credit limit constratint for diff faculties"""

    CREDIT_LIMITS = {
        Faculty.KSAS:{
            'normal': 19.0,
            'overload' : 19.0, #ksas doesnt allow overload
        },
        Faculty.EN:{
            'normal' : 19.5,
            'overload' : 23.5, 
        }
    }

def generate_schedules(courses, max_schedules=5):
    results = []

    def backtrack(i, current):
        if len(results) >= max_schedules:
            return

        if i == len(courses):
            results.append(list(current))
            return

        course = courses[i]
        for section in course.sections:
            if all(not sections_overlap(section, s) for s in current):
                current.append(section)
                backtrack(i + 1, current)
                current.pop()

    backtrack(0, [])
    return results
