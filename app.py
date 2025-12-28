from flask import Flask, render_template, request
from schedulr.solver import generate_schedules

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    schedules = None
    if request.method == "POST":
        courses = request.form.getlist("course[]")
        sections = request.form.getlist("section[]")
        # You would parse this into your Python objects
        schedules = generate_schedules(courses, sections)
    return render_template("index.html", schedules=schedules)

if __name__ == "__main__":
    app.run(debug=True)
