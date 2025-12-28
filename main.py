import json
from schedulr.models import Course, Section, MeetingTime
from schedulr.solver import generate_schedules

def load_courses(path):
    with open(path) as f:
        data = json.load(f)

    courses = []
    for c in data["courses"]:
        sections = []
        for s in c["sections"]:
            meetings = [
                MeetingTime(m["day"], m["start"], m["end"])
                for m in s["meetings"]
            ]
            sections.append(Section(s["section_id"], meetings))
        courses.append(Course(c["course_id"], c["priority"], sections))
    return courses


def print_schedule(schedule, courses):
    for section, course in zip(schedule, courses):
        print(f"{course.course_id} — Section {section.section_id}")
        for m in section.meetings:
            print(f"  {m.day} {m.start}-{m.end}")
    print()


if __name__ == "__main__":
    courses = load_courses("data/courses.json")
    schedules = generate_schedules(courses)

    for i, sched in enumerate(schedules, 1):
        print(f"Schedule #{i}")
        print_schedule(sched, courses)
