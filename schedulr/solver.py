from schedulr.constraints import sections_overlap, meetings_overlap
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

    def __init__(self, faculty, overloaded=False):
        self.faculty = faculty
        self.overloaded = overloaded
        self.max_credits = self.get_max_credits()

    def get_max_credits(self):
        limits = self.CREDIT_LIMITS[self.faculty]
        return limits['overload'] if self.overloaded else limits['normal']
    
    def is_valid_credit_load(self, total_creidts):
        return total_credits <= self.max_credits

def generate_schedules(courses, max_schedules=5, blocked_times = None, constraints = None):
    results = []
    sorted_courses = sorted(courses, key = lambda c: c.priority, reverse=True)

    def calculate_credits(schedule):
        return sum(section.course.credits for section in schedule)
    
    def is_valid_with_blocked_times(section):
        if not blocked_times:
            return True
        
        for meeting in section.meetings:
            for blocked in blocked_times:
                if meetings_overlap(meeting, blocked):
                    return False
    
    def is_within_credit_limit(schedule):
        if not constraints:
            return True
        
        total_credits = calculate_credits(schedule)
        return constraints.is_valid_credit_load(total_credits)

    def backtrack(i, current):
        if len(results) >= max_schedules:
            return

        if i == len(courses):
            if is_within_credit_limit(current):
                results.append({
                    'sections' : list(current),
                    'credits' : calculate_credits(current) if constraints else None
                })
            return
        course = sorted_courses[i]

        for section in course.sections:
            if not is_valid_with_blocked_times(section):
                continue

            if all(not sections_overlap(section, s) for s in current):
                current.append(section)
                backtrack(i + 1, current)
                current.pop()
                
        backtrack(i+1, current)

    backtrack(0, [])
    return results
