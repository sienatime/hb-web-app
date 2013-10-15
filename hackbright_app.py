import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    return """\
Title: %s 
Description: %s
Maximum Grade = %d
""" % (row[0], row[1], row[2])

def get_grade_by_student_and_project(first_name, last_name, project_title):
    query = """SELECT grade FROM grades 
    INNER JOIN students
    ON grades.student_github = students.github
    WHERE students.first_name = ? AND students.last_name = ? AND project_title = ?"""
    DB.execute(query, (first_name, last_name, project_title))
    row = DB.fetchone()
    return """\
Student: %s %s
Project: %s
Grade = %d
""" % (first_name, last_name, project_title, row[0])

def get_all_students():
    query = """SELECT * FROM Students"""
    DB.execute(query,)
    rows = DB.fetchall()
    return rows

def get_students_and_grades_by_project(project_title):
    query = """SELECT student_github, grade FROM Grades WHERE project_title=?"""
    DB.execute(query, (project_title,))
    rows = DB.fetchall()
    return rows


def show_grade_by_student(github):
    query = """SELECT project_title, grade from grades WHERE student_github = ?"""
    DB.execute(query, (github,))
    rows = DB.fetchall()
    # return rows
    return rows

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query, (first_name,last_name, github))

    CONN.commit()
    return "Successfully added student: %s %s" %(first_name, last_name) 

def make_new_project(title, description, max_grade):
    query = """INSERT into projects values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))

    CONN.commit()
    return "Successfully added project: %s" %(title)

def assign_grade_to_student(github, project_title, grade):
    query = """INSERT into grades values (?,?,?)"""
    DB.execute(query, (github, project_title, grade))

    CONN.commit()
    return "Successfully added grade: %s"%grade

def connect_to_db(): 
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        if command in ("new_project", "assign_grade") and len(tokens) > 4:
            token_str = " "
            tokens[2] = token_str.join(tokens[2:-1])
            tokens[3] = tokens[-1]
            for i in range(4, len(tokens)):
                tokens.pop()        
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "project":
            get_project_by_title(*args)
        elif command == "grade":
            get_grade_by_student_and_project(*args)
        elif command == "new_student":
            make_new_student(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "assign_grade":
            assign_grade_to_student(*args)
        elif command == "show_grade":
            show_grade_by_student(*args)


    CONN.close()

if __name__ == "__main__":
    main()
