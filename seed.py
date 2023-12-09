from faker import Faker
import psycopg2
from psycopg2 import DatabaseError
import random
from datetime import datetime, timedelta
import logging

conn = psycopg2.connect(
    dbname='WEB7',
    user='postgres',
    password='123321',
    host="localhost",
    port="5432"
)

cur = conn.cursor()
fake = Faker('uk_UA')

groups = ['Группа 1', 'Группа 2', 'Группа 3']
students_count = random.randint(30, 50)
teachers_count = random.randint(3, 5)
subjects_count = random.randint(5, 8)

try:
    for group_name in groups:
        cur.execute('INSERT INTO groups (name) VALUES (%s)', (group_name,))
    conn.commit()
except DatabaseError as e:
    conn.rollback()
    logging.error(e)

try:
    cur.execute('ALTER TABLE teachers ADD COLUMN group_id INTEGER REFERENCES groups(group_id)')
    conn.commit()
except DatabaseError as e:
    conn.rollback()
    logging.error(e)

try:
    for _ in range(subjects_count):
        cur.execute('INSERT INTO subjects (name) VALUES (%s)', (fake.name(),))
    conn.commit()
except DatabaseError as e:
    conn.rollback()
    logging.error(e)

try:
    for _ in range(teachers_count):
        group_id = random.randint(1, len(groups))
        cur.execute('INSERT INTO teachers (full_name, group_id) VALUES (%s, %s)', (fake.name(), group_id))
    conn.commit()
except DatabaseError as e:
    conn.rollback()
    logging.error(e)

try:
    for _ in range(students_count):
        group_id = random.randint(1, len(groups))
        cur.execute('INSERT INTO students (full_name, group_id) VALUES (%s,%s) RETURNING student_id', (fake.name(), group_id))
        student_id = cur.fetchone()[0]

        for sub_id in range(1, subjects_count + 1):
            for _ in range(random.randint(10, 20)):
                grade = random.randint(1, 100)
                date = fake.date_between(start_date='-1y', end_date='today')
                cur.execute('INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s)',
                            (student_id, sub_id, grade, date))
        conn.commit()

except DatabaseError as e:
    conn.rollback()
    logging.error(e)

try:
    cur.execute('ALTER TABLE teachers DROP COLUMN group_id')
    conn.commit()
except DatabaseError as e:
    conn.rollback()
    logging.error(e)

try:
    cur.execute('ALTER TABLE teachers ADD COLUMN group_id INTEGER REFERENCES groups(group_id)')
    conn.commit()
except DatabaseError as e:
    conn.rollback()
    logging.error(e)

try:
    # Додаємо колонку teacher_id у таблицю subjects, якщо вона ще не існує
    cur.execute('ALTER TABLE subjects ADD COLUMN IF NOT EXISTS teacher_id INTEGER REFERENCES teachers(teacher_id)')
    conn.commit()
except DatabaseError as e:
    conn.rollback()
    logging.error(e)

try:
    # Оновлюємо дані в колонці teacher_id для кожного предмету, прив'язуючи їх до випадкового вчителя
    for subject_id in range(1, subjects_count + 1):
        teacher_id = random.randint(1, teachers_count)  # Вибираємо випадкового вчителя
        cur.execute('UPDATE subjects SET teacher_id = %s WHERE id = %s', (teacher_id, subject_id))
    conn.commit()
except DatabaseError as e:
    conn.rollback()
    logging.error(e)
finally:
    cur.close()
    conn.close()