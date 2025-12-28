from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Your existing classes
class MeetingTime:
    def __init__(self, day, start, end):
        self.day = day
        self.start = self._parse_time(start)
        self.end = self._parse_time(end)
    
    def _parse_time(self, time_str):
        """Parse time string like '09:00' or '1:30 PM'"""
        if isinstance(time_str, str):
            try:
                return datetime.strptime(time_str, '%H:%M').time()
            except:
                return datetime.strptime(time_str, '%I:%M %p').time()
        return time_str  # Already a time object

class Section:
    def __init__(self, section_id, meetings):
        self.section_id = section_id
        self.meetings = meetings

class Course:
    def __init__(self, course_id, priority, sections):
        self.course_id = course_id
        self.priority = priority
        self.sections = sections

# Your existing helper functions
def meetings_overlap(m1, m2):
    if m1.day != m2.day:
        return False
    return not (m1.end <= m2.start or m2.end <= m1.start)

def sections_overlap(sec1, sec2):
    for m1 in sec1.meetings:
        for m2 in sec2.meetings:
            if meetings_overlap(m1, m2):
                return True
    return False

# Your scheduling algorithm
def generate_schedules(courses, max_schedules=5):
    # Sort courses by priority (higher first)
    sorted_courses = sorted(courses, key=lambda c: c.priority, reverse=True)
    results = []

    def backtrack(i, current):
        if len(results) >= max_schedules:
            return

        if i == len(sorted_courses):
            results.append(list(current))
            return

        course = sorted_courses[i]
        for section in course.sections:
            if all(not sections_overlap(section, s) for s in current):
                current.append(section)
                backtrack(i + 1, current)
                current.pop()

    backtrack(0, [])
    return results

# Helper function to check blocked times
def section_conflicts_with_blocked(section, blocked_times):
    """Check if a section conflicts with any blocked times"""
    for meeting in section.meetings:
        for blocked in blocked_times:
            blocked_meeting = MeetingTime(blocked['day'], blocked['start'], blocked['end'])
            if meetings_overlap(meeting, blocked_meeting):
                return True
    return False

def generate_schedules_with_blocked(courses, blocked_times=None, max_schedules=5):
    """Generate schedules considering blocked times"""
    if blocked_times:
        # Filter out sections that conflict with blocked times
        filtered_courses = []
        for course in courses:
            valid_sections = [s for s in course.sections 
                            if not section_conflicts_with_blocked(s, blocked_times)]
            if valid_sections:
                filtered_courses.append(
                    Course(course.course_id, course.priority, valid_sections)
                )
        courses = filtered_courses
    
    return generate_schedules(courses, max_schedules)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    
    # Parse courses from JSON
    courses = []
    for course_data in data['courses']:
        sections = []
        for section_data in course_data['sections']:
            meetings = []
            for time_data in section_data['times']:
                meetings.append(MeetingTime(
                    time_data['day'],
                    time_data['start'],
                    time_data['end']
                ))
            sections.append(Section(section_data['id'], meetings))
        
        courses.append(Course(
            course_data['name'],
            course_data['priority'],
            sections
        ))
    
    # Parse blocked times
    blocked_times = data.get('blockedTimes', [])
    max_schedules = data.get('maxSchedules', 10)
    
    # Generate schedules using your algorithm
    schedules = generate_schedules_with_blocked(courses, blocked_times, max_schedules)
    
    # Convert schedules to JSON-friendly format
    result_schedules = []
    for schedule in schedules:
        schedule_data = []
        for section in schedule:
            # Find the course for this section
            course = next(c for c in courses if section in c.sections)
            schedule_data.append({
                'course': course.course_id,
                'section': section.section_id,
                'times': [
                    {
                        'day': m.day,
                        'start': m.start.strftime('%H:%M'),
                        'end': m.end.strftime('%H:%M')
                    }
                    for m in section.meetings
                ]
            })
        result_schedules.append(schedule_data)
    
    return jsonify({
        'success': True,
        'count': len(result_schedules),
        'schedules': result_schedules
    })

if __name__ == '__main__':
    app.run(debug=True)