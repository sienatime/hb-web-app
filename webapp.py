from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("student")

    kwargs = {}
    
    if request.args.get("grade") and request.args.get("project_title"):
        #then set the thing in the database and render it in the html
        project_title = request.args.get("project_title")
        grade = request.args.get("grade")
        hackbright_app.assign_grade_to_student(student_github, project_title, grade)
        kwargs["project_title"]=project_title
        kwargs["grade"]=grade

    row = hackbright_app.get_student_by_github(student_github)
    grades_row = hackbright_app.show_grade_by_student(student_github)
    kwargs = {"first_name" : row[0], "last_name" : row[1], "github" : row[2], "grade_rows" : grades_row}
    html = render_template("student_info.html", **kwargs)
    return html

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/project")
def get_grades_by_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")
    kwargs = {}
    
    if request.args.get("grade") and request.args.get("github"):
        #then set the thing in the database and render it in the html
        github = request.args.get("github")
        grade = request.args.get("grade")
        hackbright_app.assign_grade_to_student(github, project_title, grade)
        kwargs["github"]=github
        kwargs["grade"]=grade

    rows = hackbright_app.get_students_and_grades_by_project(project_title)
    kwargs = {"project_title":project_title, "project_rows":rows}
    html = render_template("project.html", **kwargs)
    return html

@app.route("/test")
def test_handler():
    return "test"

@app.route("/newstudent")
def new_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    hackbright_app.make_new_student(first_name, last_name, github)
    html = render_template("new_student.html", first_name=first_name, 
                                               last_name=last_name, 
                                               github=github)
    return html

@app.route("/newproject")
def new_project():
    hackbright_app.connect_to_db()
    title = request.args.get("title")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")
    hackbright_app.make_new_project(title, description, max_grade)
    html = render_template("new_project.html", title=title,
                                                description=description,
                                                max_grade=max_grade)
    return html

@app.route("/gradestudent")
def grade_student():
    hackbright_app.connect_to_db()
    github = request.args.get("github")
    project_title = request.args.get("project_title")
    grade = request.args.get("grade")
    hackbright_app.assign_grade_to_student(github, project_title, grade)
    html = render_template("grade_student.html", github=github,
                                                project_title=project_title,
                                                grade=grade)
    return html

@app.route("/allstudents")
def get_all_students():
    hackbright_app.connect_to_db()
    rows = hackbright_app.get_all_students()
    return render_template("all_students.html", student_data = rows)

@app.route("/allprojects")
def get_all_projects():
    hackbright_app.connect_to_db()
    rows = hackbright_app.get_all_projects()
    return render_template("all_projects.html", project_data = rows)


if __name__ == "__main__":
    app.run(debug=True)