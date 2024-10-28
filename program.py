import sqlite3

conn = sqlite3.connect('university.db')
cursor = conn.cursor()


def create_database():
    cursor.execute('''
        CREATE TABLE  IF NOT EXISTS  Students
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        department TEXT NOT NULL,
        date_of_birth DATE NOT NULL
    );''')

    cursor.execute('''
        CREATE TABLE  IF NOT EXISTS Teachers
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        department TEXT NOT NULL
    );''')

    cursor.execute('''
        CREATE TABLE  IF NOT EXISTS Courses
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id)  REFERENCES Teachers (id)
    );''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Exams
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_of_exam DATE NOT NULL,
        course_id INTEGER,
        max_score INTEGER,
        FOREIGN KEY (course_id)  REFERENCES Courses (id)
    );''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Grades
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_ID INTEGER,
        exam_ID INTEGER,
        score INTEGER NOT NULL,
        FOREIGN KEY (student_ID)  REFERENCES Students (id),
        FOREIGN KEY (exam_ID)  REFERENCES Exams (id)
    );''')

    conn.commit()


def add_student(name, surname, department, date_of_birth):
    cursor.execute("INSERT INTO Students (name, surname, department, date_of_birth) VALUES (?, ?, ?, ?)",
                   (name, surname, department, date_of_birth))
    conn.commit()


def add_teacher(name, surname, department):
    cursor.execute("INSERT INTO Teachers (name, surname, department) VALUES (?, ?, ?)",
                   (name, surname, department))
    conn.commit()


def add_course(title, description, teacher_id):
    cursor.execute("INSERT INTO Courses (title, description, teacher_id) VALUES (?, ?, ?)",
                   (title, description, teacher_id))
    conn.commit()


def add_exam(date, course_id, max_score):
    cursor.execute("INSERT INTO Exams (date_of_exam, course_id, max_score) VALUES (?, ?, ?)",
                   (date, course_id, max_score))
    conn.commit()


def add_grade(student_id, exam_id, score):
    cursor.execute("INSERT INTO Grades (student_id, exam_id, score) VALUES (?, ?, ?)",
                   (student_id, exam_id, score))
    conn.commit()


def update_student(student_id, name, surname, department, date_of_birth):
    cursor.execute("UPDATE Students SET name = ?, surname = ?, department = ?, date_of_birth = ? WHERE id = ?",
                   (name, surname, department, date_of_birth, student_id))
    conn.commit()


def update_teacher(teacher_id, name, surname, department):
    cursor.execute("UPDATE Teachers SET name = ?, surname = ?, department = ? WHERE id = ?",
                   (name, surname, department, teacher_id))
    conn.commit()


def update_course(course_id, title, description, teacher_id):
    cursor.execute("UPDATE Courses SET title = ?, description = ?, teacher_id = ? WHERE id = ?",
                   (title, description, teacher_id, course_id))
    conn.commit()


def delete_student(student_id):
    cursor.execute("DELETE FROM Students WHERE id = ?", (student_id,))
    conn.commit()


def delete_teacher(teacher_id):
    cursor.execute("DELETE FROM Teachers WHERE id = ?", (teacher_id,))
    conn.commit()


def delete_course(course_id):
    cursor.execute("DELETE FROM Courses WHERE id = ?", (course_id,))
    conn.commit()


def delete_exam(exam_id):
    cursor.execute("DELETE FROM Exams WHERE id = ?", (exam_id,))
    conn.commit()


def get_students_by_department(department):
    cursor.execute("SELECT * FROM Students WHERE department = ?", (department,))
    return cursor.fetchall()


def get_courses_by_teacher(teacher_id):
    cursor.execute("SELECT * FROM Courses WHERE teacher_id = ?", (teacher_id,))
    return cursor.fetchall()


def get_students_by_course(course_id):
    cursor.execute('''
    SELECT DISTINCT student.* 
    FROM Students AS student
    JOIN Grades AS grade ON student.id = grade.student_id
    JOIN Exams AS exam ON grade.exam_id = exam.id
    JOIN Courses AS course ON exam.course_id = course.id
    WHERE course.id = ?
    ''', (course_id,))
    return cursor.fetchall()


def get_grades_by_course(course_id, student_id):
    cursor.execute('''
    SELECT grade.score, exam.date_of_exam, course.title
    FROM Grades AS grade
    JOIN Exams AS exam ON grade.exam_id = exam.id
    JOIN Courses AS course ON exam.course_id = course.id
    WHERE course.id = ? AND grade.student_id = ?
    ''', (course_id, student_id))
    return cursor.fetchall()


def get_average_score_by_course_and_student(course_id, student_id):
    cursor.execute('''
    SELECT AVG(grade.score)
    FROM Students AS student
    JOIN Grades AS grade ON student.id = grade.student_id
    JOIN Exams AS exam ON grade.exam_id = exam.id
    JOIN Courses AS course ON exam.course_id = course.id
    WHERE student.id = ? AND course.id = ?
    ''', (student_id, course_id))
    return cursor.fetchone()[0]


def get_average_score_by_student(student_id):
    cursor.execute("SELECT AVG(Score) FROM Grades WHERE student_id = ?",
                   (student_id,))
    return cursor.fetchone()[0]


def get_average_score_by_department(department):
    cursor.execute('''
        SELECT AVG(grade.Score) FROM Grades AS grade
        JOIN Students AS student ON grade.student_id = student.id
        WHERE student.department = ?
        ''', (department,))
    return cursor.fetchone()[0]


def delete_students():
    cursor.execute("DROP TABLE Students")


def delete_teachers():
    cursor.execute("DROP TABLE Teachers")


def delete_exams():
    cursor.execute("DROP TABLE Exams")


def delete_courses():
    cursor.execute("DROP TABLE Courses")


def delete_grades():
    cursor.execute("DROP TABLE Grades")


def delete_database():
    delete_students()
    delete_teachers()
    delete_courses()
    delete_exams()
    delete_grades()
    create_database()


create_database()

while True:
    print("\nВыберите действие:")
    print("1. Добавить студента")
    print("2. Изменить студента")
    print("3. Удалить студента")
    print("4. Получить список студентов по факультету")
    print("5. Получить список студентов, зачисленных на конкретный курс")
    print("6. Добавить преподавателя")
    print("7. Изменить преподавателя")
    print("8. Удалить преподавателя")
    print("9. Добавить курс")
    print("10. Изменить курс")
    print("11. Удалить курс")
    print("12. Получить список курсов, читаемых определенным преподавателем")
    print("13. Добавить экзамен")
    print("14. Удалить экзамен")
    print("15. Добавить оценку")
    print("16. Получить оценки студентов по определенному курсу")
    print("17. Получить средний бал студента по определенному курсу")
    print("18. Получить средний бал студента в целом")
    print("19. Получить средний был по факультету")
    print("20. Удалить данные")
    print("21. Выйти")

    user_choice = input("\nВыберите действие: ")

    match user_choice:

        case "1":

            name = input("Введите имя студента: ")
            surname = input("Введите фамилию студента: ")
            department = input("Введите факультет студента: ")
            date_of_birth = input("Введите дату рождения студента в формате (YYYY-MM-DD): ")

            add_student(name, surname, department, date_of_birth)

        case "2":

            student_id = int(input("Введите id студента: "))
            new_name = input("Введите новое имя студента: ")
            new_surname = input("Введите новую фамилию студента: ")
            new_department = input("Введите новое отделение студента: ")
            new_date_of_birth = input("Введите новую дату рождения студента в формате (YYYY-MM-DD): ")

            update_student(student_id, new_name, new_surname, new_department, new_date_of_birth)

        case "3":

            student_id = int(input("Введите id студента: "))

            delete_student(student_id)
            print(f"Студент с id {student_id} был удален")

        case "4":
            department = input("Введите факультет: ")

            students = get_students_by_department(department)
            for student in students:
                print(student)

        case "5":

            course = input("Введите номер курса: ")
            get_students_by_course(course)

        case "6":

            name = input("Введите имя преподавателя: ")
            surname = input("Введите фамилию преподавателя: ")
            department = input("Введите кафедру преподавателя: ")

            add_teacher(name, surname, department)

        case "7":

            teacher_id = int(input("Введите id преподавателя: "))
            new_name = input("Введите новое имя преподавателя: ")
            new_surname = input("Введите новую фамилию преподавателя: ")
            new_department = input("Введите новую кафеду преподавателя: ")

            update_teacher(teacher_id, new_name, new_surname, new_department)

        case "8":

            teacher_id = int(input("Введите id преподавателя: "))

            delete_teacher(teacher_id)
            print(f"Преподаватель с id {teacher_id} был удален")

        case "9":

            title = input("Введите название курса: ")
            description = input("Введите описание курса: ")
            teacher_id = int(input("Введите id преподавателя: "))

            add_teacher(title, description, teacher_id)

        case "10":

            course_id = int(input("Введите id курса: "))
            new_title = input("Введите новое название курса: ")
            new_description = input("Введите новое описание курса: ")
            teacher_id = int(input("Введите id преподавателя: "))

            update_course(course_id, new_title, new_description, teacher_id)

        case "11":

            course_id = int(input("Введите id курса: "))

            delete_course(course_id)
            print(f"курс с id {course_id} был удален")

        case "12":

            teacher_id = int(input("Введите id преподавателя: "))

            courses = get_courses_by_teacher(teacher_id)
            for course in courses:
                print(course)

        case "13":

            date = input("Введите дату экзамена в формате(YYYY-MM-DD): ")
            course_id = int(input("Введите id курса: "))
            max_score = int(input("Введите максимальный балл: "))

            add_exam(date, course_id, max_score)

        case "14":

            exam_id = int(input("Введите id экзамена: "))

            delete_exam(exam_id)
            print(f"экзамен с id {exam_id} был удален")

        case "15":

            student_id = int(input("Введите id студента: "))
            exam_id = int(input("Введите id экзамена: "))
            score = int(input("Введите результат: "))

            add_grade(student_id, exam_id, score)

        case "16":

            course_id = int(input("Введите id курса: "))
            student_id = int(input("Введите id студента: "))

            grades = get_grades_by_course(course_id, student_id)
            for grade in grades:
                print(grade)

        case "17":

            course_id = int(input("Введите id курса: "))
            student_id = int(input("Введите id студента: "))

            get_average_score_by_course_and_student(course_id, student_id)

        case "18":

            student_id = int(input("Введите id студента: "))

            get_average_score_by_student(student_id)

        case "19":

            department = input("Введите факультет: ")

            get_average_score_by_department(department)

        case "20":
            delete_database()
            print("Данные были удалены")

        case "21":
            print("Выполнен выход")
            break

cursor.close()
conn.close()
