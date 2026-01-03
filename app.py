from flask import Flask, render_template, request, jsonify
from datetime import datetime
from schedulr.models import Course, Section, MeetingTime
from schedulr.solver import generate_schedules, ScheduleConstraints, Faculty
from schedulr.constraints import meetings_overlap

app = Flask(__name__)

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
            sections,
            credits=course_data.get('credits', 3.0)  # ADD THIS
        ))
    
    # Parse blocked times
    blocked_times = []
    for blocked in data.get('blockedTimes', []):
        blocked_times.append(MeetingTime(
            blocked['day'],
            blocked['start'],
            blocked['end']
        ))
    
    # Parse constraints
    constraints = None
    if 'faculty' in data:
        faculty = Faculty.KSAS if data['faculty'] == 'ksas' else Faculty.EN
        allow_overload = data.get('allowOverload', False)
        constraints = ScheduleConstraints(faculty, allow_overload)
    
    max_schedules = data.get('maxSchedules', 10)
    
    # Generate schedules using your algorithm
    schedules = generate_schedules(
        courses, 
        max_schedules=max_schedules,
        blocked_times=blocked_times if blocked_times else None,
        constraints=constraints
    )
    
    # Convert schedules to JSON-friendly format
    result_schedules = []
    for schedule_data in schedules:
        schedule = []
        sections = schedule_data['sections'] if isinstance(schedule_data, dict) else schedule_data
        
        for section in sections:
            course = section.course
            schedule.append({
                'course': course.course_id,
                'section': section.section_id,
                'credits': course.credits,
                'times': [
                    {
                        'day': m.day,
                        'start': m.start,
                        'end': m.end
                    }
                    for m in section.meetings
                ]
            })
        
        result_schedules.append({
            'sections': schedule,
            'total_credits': schedule_data.get('credits') if isinstance(schedule_data, dict) else None
        })
    
    return jsonify({
        'success': True,
        'count': len(result_schedules),
        'schedules': result_schedules
    })

if __name__ == '__main__':
    app.run(debug=True)