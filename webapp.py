from flask import Flask, render_template, request, redirect
import hackbright_app

app = Flask(__name__)

#home page. has a bunch of forms on it
@app.route("/")
def get_github():
    return render_template("get_github.html")

#shows info on a particular student
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

#shows info on a particular project
@app.route("/project")
def get_grades_by_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")
    rows = hackbright_app.get_students_and_grades_by_project(project_title)
    html = render_template("project.html", project_title=project_title, project_rows=rows)
    return html

# This is a post method that assigns a grade to a student and then redirects to the project page
@app.route("/grade", methods=['POST'])
def grade_student():
    github = request.form.get("github")
    grade = request.form.get("grade")
    project_title = request.form.get("project_title")
    print "webapp.py", github, project_title, grade
    hackbright_app.assign_grade_to_student(github, project_title, grade)
    print "**********", request.referrer
    if "project" in request.referrer:
        return redirect('/project?project_title='+project_title)
    elif "student" in request.referrer:
        return redirect('/student?student='+github)

# post method that creates a new student and then redirects to their student info page
@app.route("/newstudent", methods=['POST'])
def new_student():
    hackbright_app.connect_to_db()
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")
    hackbright_app.make_new_student(first_name, last_name, github)

    return redirect("/student?student="+github)

# post method that creates a new project then redirects to the project page
@app.route("/newproject", methods=['POST'])
def new_project():
    hackbright_app.connect_to_db()
    title = request.form.get("title")
    description = request.form.get("description")
    max_grade = request.form.get("max_grade")
    hackbright_app.make_new_project(title, description, max_grade)
                              
    return redirect("/project?project_title="+title)

# show all the students
@app.route("/allstudents")
def get_all_students():
    hackbright_app.connect_to_db()
    rows = hackbright_app.get_all_students()
    return render_template("all_students.html", student_data = rows)

#show all the projects
@app.route("/allprojects")
def get_all_projects():
    hackbright_app.connect_to_db()
    rows = hackbright_app.get_all_projects()
    return render_template("all_projects.html", project_data = rows)

if __name__ == "__main__":
    app.run(debug=True)