"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect, flash

import hackbright

app = Flask(__name__)
app.secret_key = "secretsecretsecret"


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    student_grades = hackbright.get_grades_by_github(github)

    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           student_grades=student_grades)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def student_add():
    """Add a student."""

    return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def confirm_student_added():
    """Confirm that student has been added."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    success = hackbright.make_new_student(first_name, last_name, github)
    flash(success)

    return redirect("/student?github=" + github)


@app.route("/project/<project>")
def display_project_info(project):
    """Display information about a project."""

    title, description, max_grade = hackbright.get_project_by_title(project)

    student_github = hackbright.get_grades_by_title(project)

    print "github:", student_github

    return render_template('project_info.html',
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           student_github=student_github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
