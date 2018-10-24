"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash

import hackbright


app = Flask(__name__)

@app.route("/")
def display_homepage():
	"""List all the students and list all the projects"""
	students = hackbright.get_all_students()

	projects = hackbright.get_all_projects()

	return render_template("homepage.html", students=students, projects=projects)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    # return a list of tuples of project and grade for the github user
    grade_listing = hackbright.get_grades_by_github(github)

    return render_template("student_info.html", first=first, last=last, github=github, projects= grade_listing)


@app.route("/add-student", methods=["POST"])
def add_student():
	"""Add new student to the database"""

	firstname = request.form.get('firstname')
	lastname = request.form.get('lastname')
	github = request.form.get('github')

	hackbright.make_new_student(firstname, lastname, github)

	return render_template("addstudent-thankyou.html", firstname=firstname, lastname=lastname, github=github)


@app.route("/project", methods=["GET"])
def show_project():
	"""Display information about the project (title, description, max grade)"""

	# TO DO: maybe add something to check whether the title exists in the database? or does it do this already?
	title = request.args.get('title')

	# unpacking from the get_project_by_title function
	title, description, max_grade = hackbright.get_project_by_title(title)

	# get all the students that completed that project from the get_grades_by_title function
	grades = hackbright.get_grades_by_title(title)

	return render_template("project_info.html", title=title, description=description, max_grade=max_grade, grades=grades)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
