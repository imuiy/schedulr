class MeetingTime:
    def __init__(self, day, start, end):
        self.day = day
        self.start = start
        self.end = end


class Section:
    def __init__(self, section_id, meetings):
        self.section_id = section_id
        self.meetings = meetings
        self.course = None


class Course:
    def __init__(self, course_id, priority, sections, credits=3.0):  # ADD credits=3.0 HERE
        self.course_id = course_id
        self.priority = priority
        self.sections = sections
        self.credits = credits  # This was trying to use 'credits' before it was passed in

        for section in sections:
            section.course = self