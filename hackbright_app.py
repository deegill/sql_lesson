import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])
    return row

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successssss you added student: %s %s" % (first_name, last_name)

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("my_database.db")
    DB = CONN.cursor()

def get_project_by_project_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Project: %s 
Description: %s"""%(row[0], row[1]) 

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "You're so awesome you just added the project %s" % title 

def get_student_grade_by_project(title):
    query = """SELECT first_name, last_name, grade FROM ReportCardView WHERE title=?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print"""\
%s %s got an awesome grade offfff......: %s"""%(row[0], row[1], row[2])

def give_student_grade(github, title, grade):
    query = """INSERT into Grades values(?, ?, ?) """
    DB.execute(query,(github, title, grade))
    CONN.commit()
    print "%s got a grade of %s on %s project" %(github, grade, title)    

def show_grades_by_student(github):
    student_info = get_student_by_github(github)
    query = """SELECT project_title, grade FROM Grades WHERE student_github=?"""
    DB.execute(query, (github,))
    row = DB.fetchall()
    for i in range(len(row)):
        print """%s %s got a %s on %s""" %(student_info[0], student_info[1], row[i][1], row[i][0])

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_project_title(*args)
        elif command == "new_project":
            joined_list = ' '.join(args).split(',')
            args = joined_list
            make_new_project(*args)
        elif command == "student_grade":
            get_student_grade_by_project(*args)
        elif command == "grading":
            give_student_grade(*args)
        elif command == "show_grades":
            show_grades_by_student(*args)

    CONN.close()

if __name__ == "__main__":
    main()
