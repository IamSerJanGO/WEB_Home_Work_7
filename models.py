from sqlalchemy import Column, Integer, String, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True)
    name = Column(String(70), nullable=False)
    students = relationship('Student', back_populates='group')

class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.group_id'))
    group = relationship('Group', back_populates='students')

class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    subjects = relationship('Subject', back_populates='teacher')

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(70), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'))
    teacher = relationship('Teacher', back_populates='subjects')
    grades = relationship('Grade', back_populates='subject')

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Integer, CheckConstraint('grade >= 0 AND grade <= 100'))
    grade_date = Column(Date, nullable=True)

    subject = relationship('Subject')
