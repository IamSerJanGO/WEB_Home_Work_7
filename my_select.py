from main import session
from models import *
from sqlalchemy import func, desc
from sqlalchemy.orm import joinedload

# Предполагается, что у вас уже есть созданная сессия 'session'
def select_1(session):
    result = session.query(
        Student.full_name,
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).select_from(Grade).join(Student).group_by(Student.student_id).order_by(desc('avg_grade')).limit(5).all()

    return result

def select_2(session):
    subject_input = input('Введите название предмета: ')
    subject = session.query(Subject).filter_by(name=subject_input).first()
    if subject:
        subject_id = subject.id

        result = (
            session.query(Student.full_name, func.avg(Grade.grade).label('avg_grade'))
            .join(Grade)
            .filter(Grade.subject_id == subject_id)
            .group_by(Student.student_id)
            .order_by(func.avg(Grade.grade).desc())
            .limit(1)
            .first()
        )

        if result:
            student_name, avg_grade = result
            print(f"Студент {student_name} имеет самый высокий средний балл по предмету {subject_name}.")
            print(f"Средний балл: {avg_grade}")
        else:
            print(f"Студенты по предмету {subject_name} отсутствуют в базе данных.")
    else:
        print(f"Предмет {subject_name} не найден в базе данных.")

def select_3(session):
    user_input = input('Введите название предмета: ')
    subject = session.query(Subject).filter_by(name=user_input).first()
    if subject:
        result = (
            session.query(Group.name, func.avg(Grade.grade))
            .select_from(Group)
            .join(Student, Student.group_id == Group.group_id)
            .join(Grade, Grade.student_id == Student.student_id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.name == user_input)
            .group_by(Group.name)
            .all()
        )
        return result


def select_4(session):
    return session.query(func.avg(Grade.grade)).scalar()

def select_5(session):
    teacher_name = input('Введите имя препода: ')
    teacher = session.query(Teacher).filter_by(full_name=teacher_name).first()
    if teacher:
        teacher_id = teacher.teacher_id
        courses = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
        return courses


def select_6(session):
    group_name = input('Введите название группы: ')
    group = session.query(Group).filter_by(name=group_name).first()
    if group:
        students = session.query(Student).filter_by(group_id=group.group_id).all()
        return [student.full_name for student in students]
    else:
        return f"Группа {group_name} не найдена в базе данных."


def select_7(session):
    group_name = input('Введите название группы: ')
    subject_name = input('Введите название предмета: ')

    group = session.query(Group).filter_by(name=group_name).first()
    subject = session.query(Subject).filter_by(name=subject_name).first()

    if group and subject:
        grades = (
            session.query(Student.full_name, Grade.grade)
            .join(Grade)
            .join(Subject)
            .join(Group)
            .filter(Group.group_id == group.group_id, Subject.id == subject.id)
            .all()
        )

        result = {}
        for student_name, grade in grades:
            if student_name not in result:
                result[student_name] = []
            result[student_name].append(grade)

        return result

def select_8(session):
    teacher_name = input('Введите имя преподавателя: ')

    teacher = session.query(Teacher).filter_by(full_name=teacher_name).first()

    if teacher:
        teacher_id = teacher.teacher_id

        avg_grade = (
            session.query(func.avg(Grade.grade))
            .join(Subject)
            .join(Teacher)
            .filter(Teacher.teacher_id == teacher_id)
            .scalar()
        )

        return f"Средний балл, который ставит {teacher_name} по своим предметам: {avg_grade:.2f}" if avg_grade else "Преподаватель не имеет оценок по своим предметам."

def select_9(session):
    student_name = input('Введите имя студента: ')

    student = session.query(Student).filter_by(full_name=student_name).first()

    if student:
        student_id = student.student_id

        courses = (
            session.query(Subject.name)
            .join(Grade)
            .filter(Grade.student_id == student_id)
            .distinct()
            .all()
        )

        if courses:
            courses_list = [course.name for course in courses]
            return f"Студент {student_name} посещает курсы: {', '.join(courses_list)}"
        else:
            return f"Студент {student_name} не посещает ни одного курса."

def select_10(session):
    student_name = input('Введіть повне ім\'я студента: ')
    teacher_name = input('Введіть повне ім\'я викладача: ')

    student = session.query(Student).filter_by(full_name=student_name).first()
    teacher = session.query(Teacher).filter_by(full_name=teacher_name).first()

    if student and teacher:
        student_id = student.student_id
        teacher_id = teacher.teacher_id

        courses = (
            session.query(Subject.name)
            .join(Grade)
            .join(Teacher)
            .filter(Grade.student_id == student_id)
            .filter(Subject.teacher_id == teacher_id)
            .distinct()
            .all()
        )

        if courses:
            courses_list = [course.name for course in courses]
            return f"Студент {student_name} вивчає курси у викладача {teacher_name}: {', '.join(courses_list)}"
        else:
            return f"Студент {student_name} не вивчає жодного курсу у викладача {teacher_name}."
    else:
        return "Студент або викладач не знайдений в базі даних."

