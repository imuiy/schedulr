from schedulr.constraints import sections_overlap

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
