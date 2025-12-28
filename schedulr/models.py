class MeetingTime:
    def __init__(self, day, start, end):
        self.day = day
        self.start = start
        self.end = end


class Section:
    def __init__(self, section_id, meetings):
        self.section_id = section_id
        self.meetings = meetings


class Course:
    def __init__(self, course_id, priority, sections):
        self.course_id = course_id
        self.priority = priority
        self.sections = sections
