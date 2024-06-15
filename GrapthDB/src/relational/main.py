from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import time
import sys
from datetime import datetime, timedelta
from sqlalchemy.sql import text

# Создание базы данных
engine = create_engine('sqlite:///university_schedule.db')
Base = declarative_base()

# Определение таблиц
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    student_number = Column(Integer, nullable=False)
    students = relationship('Student', back_populates='group')

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    group = relationship('Group', back_populates='students')
    lesson = relationship('Lesson', back_populates='students')

class Professor(Base):
    __tablename__ = 'professors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    discipline_id = Column(Integer, ForeignKey('disciplines.id'))
    discipline = relationship('Discipline', back_populates='professors')

class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    professors = relationship('Professor', back_populates='discipline')
    lessons = relationship('Lesson', back_populates='discipline')

class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    start_time = Column(Time, nullable=False)
    duration_time = Column(Integer, nullable=False)
    max_students = Column(Integer, nullable=False)
    discipline_id = Column(Integer, ForeignKey('disciplines.id'))
    professor_id = Column(Integer, ForeignKey('professors.id'))
    discipline = relationship('Discipline', back_populates='lessons')
    professor = relationship('Professor')
    students = relationship('Student', back_populates='lesson')

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Добавление данных
Session = sessionmaker(bind=engine)
session = Session()

def add_group(name, student_number):
    group = session.query(Group).filter_by(name=name).first()
    if not group:
        group = Group(name=name, student_number=student_number)
        session.add(group)
    return group

def add_student(name, group):
    student = session.query(Student).filter_by(name=name, group_id=group.id).first()
    if not student:
        student = Student(name=name, group_id=group.id)
        session.add(student)
    return student

def add_discipline(name):
    discipline = session.query(Discipline).filter_by(name=name).first()
    if not discipline:
        discipline = Discipline(name=name)
        session.add(discipline)
    return discipline

def add_professor(name, discipline):
    professor = session.query(Professor).filter_by(name=name, discipline_id=discipline.id).first()
    if not professor:
        professor = Professor(name=name, discipline_id=discipline.id)
        session.add(professor)
    return professor

def add_lesson(start_time, duration_time, max_students, discipline, professor):
    lesson = session.query(Lesson).filter_by(start_time=start_time, duration_time=duration_time, discipline_id=discipline.id, professor_id=professor.id).first()
    if not lesson:
        lesson = Lesson(start_time=start_time, duration_time=duration_time, max_students=max_students, discipline_id=discipline.id, professor_id=professor.id)
        session.add(lesson)
    return lesson

# Примеры добавления данных
group1 = add_group('Group 1', 20)
group2 = add_group('Group 2', 25)
group3 = add_group('Group 3', 30)
session.commit()

student1 = add_student('Student 1', group1)
student2 = add_student('Student 2', group1)
student3 = add_student('Student 3', group2)
student4 = add_student('Student 4', group2)
student5 = add_student('Student 5', group3)
student6 = add_student('Student 6', group3)
session.commit()

discipline1 = add_discipline('Mathematics')
discipline2 = add_discipline('Physics')
discipline3 = add_discipline('Chemistry')
session.commit()

professor1 = add_professor('Professor 1', discipline1)
professor2 = add_professor('Professor 2', discipline2)
professor3 = add_professor('Professor 3', discipline3)
session.commit()

lesson1 = add_lesson(time(9, 0, 0), 90, 30, discipline1, professor1)
lesson2 = add_lesson(time(11, 0, 0), 90, 25, discipline2, professor2)
lesson3 = add_lesson(time(13, 0, 0), 90, 20, discipline3, professor3)
session.commit()

student1.lesson_id = lesson1.id
student2.lesson_id = lesson1.id
student3.lesson_id = lesson2.id
student4.lesson_id = lesson2.id
student5.lesson_id = lesson3.id
student6.lesson_id = lesson3.id
session.commit()

# Запросы для получения ответов

def get_average_students_per_group():
    return session.query(func.avg(Group.student_number)).scalar()

def get_average_disciplines_per_student():
    result = session.query(
        func.count(Discipline.id) / func.count(Student.id)
    ).select_from(Student).join(Group).join(Lesson, Student.lesson_id == Lesson.id).join(Discipline, Lesson.discipline_id == Discipline.id).scalar()
    return result

def get_average_disciplines_per_professor():
    result = session.query(
        func.count(Discipline.id) / func.count(Professor.id)
    ).select_from(Professor).join(Discipline).scalar()
    return result

def get_schedule_conflicts(group_id, discipline_id=None):
    # SQL запрос для поиска конфликтов в расписании
    query = text('''
    SELECT
        f.id AS first_lesson_id,
        s.id AS second_lesson_id
    FROM lessons AS f
    INNER JOIN lessons AS s
        ON f.id != s.id
        AND f.start_time < time(s.start_time, '+' || s.duration_time || ' minutes')
        AND time(f.start_time, '+' || f.duration_time || ' minutes') > s.start_time
    INNER JOIN students AS sf ON sf.lesson_id = f.id
    INNER JOIN students AS ss ON ss.lesson_id = s.id
    WHERE sf.group_id = :group_id
        AND ss.group_id = :group_id
    ''')
    if discipline_id:
        query = text('''
        SELECT
            f.id AS first_lesson_id,
            s.id AS second_lesson_id
        FROM lessons AS f
        INNER JOIN lessons AS s
            ON f.id != s.id
            AND f.start_time < time(s.start_time, '+' || s.duration_time || ' minutes')
            AND time(f.start_time, '+' || f.duration_time || ' minutes') > s.start_time
        INNER JOIN students AS sf ON sf.lesson_id = f.id
        INNER JOIN students AS ss ON ss.lesson_id = s.id
        WHERE sf.group_id = :group_id
            AND ss.group_id = :group_id
            AND f.discipline_id = :discipline_id AND s.discipline_id = :discipline_id
        ''')

    result = session.execute(query, {'group_id': group_id, 'discipline_id': discipline_id}).fetchall()

    conflicts = []
    for res in result:
        conflict_info = {
            "first_lesson_id": res.first_lesson_id,
            "second_lesson_id": res.second_lesson_id,
        }
        conflicts.append(conflict_info)

    return conflicts


def get_free_slots(group_id, professor_id, duration_minutes=120):
    # Получаем все уроки группы и профессора
    group_lessons = session.query(Lesson).join(Student).filter(Student.group_id == group_id).all()
    professor_lessons = session.query(Lesson).filter(Lesson.professor_id == professor_id).all()

    # Объединяем и сортируем все уроки по времени начала
    all_lessons = sorted(group_lessons + professor_lessons, key=lambda l: l.start_time)

    # Ищем свободные слоты
    free_slots = []
    start_of_day = time(8, 0)
    end_of_day = time(18, 0)
    last_end_time = start_of_day

    for lesson in all_lessons:
        lesson_start_time = lesson.start_time
        lesson_end_time = (datetime.combine(datetime.today(), lesson.start_time) + timedelta(minutes=lesson.duration_time)).time()

        # Проверяем свободный слот до начала текущего урока
        if datetime.combine(datetime.today(), lesson_start_time) - datetime.combine(datetime.today(), last_end_time) >= timedelta(minutes=duration_minutes):
            free_slots.append((last_end_time, lesson_start_time))

        last_end_time = lesson_end_time

    # Проверяем слот после последнего урока до конца дня
    if datetime.combine(datetime.today(), end_of_day) - datetime.combine(datetime.today(), last_end_time) >= timedelta(minutes=duration_minutes):
        free_slots.append((last_end_time, end_of_day))

    return free_slots


# Интерфейс командной строки
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <function>")
        return
    
    function = sys.argv[1]
    
    if function == "get_average_students_per_group":
        print(f'Average number of students per group: {get_average_students_per_group()}')
    elif function == "get_average_disciplines_per_student":
        print(f'Average number of disciplines per student: {get_average_disciplines_per_student()}')
    elif function == "get_average_disciplines_per_professor":
        print(f'Average number of disciplines per professor: {get_average_disciplines_per_professor()}')
    elif function == "get_schedule_conflicts":
        if len(sys.argv) < 3:
            print("Usage: python main.py get_schedule_conflicts <group_id>")
            return
        group_id = int(sys.argv[2])
        discipline_id = int(sys.argv[3])
        conflicts = get_schedule_conflicts(group_id, discipline_id)
        print(f'Schedule conflicts for group {group_id}: {conflicts}')
    elif function == "get_free_slots":
        if len(sys.argv) < 4:
            print("Usage: python main.py get_free_slots <group_id> <professor_id>")
            return
        group_id = int(sys.argv[2])
        professor_id = int(sys.argv[3])
        free_slots = get_free_slots(group_id, professor_id)
        print(f'Free slots for group {group_id} and professor {professor_id}: {free_slots}')
    else:
        print(f"Unknown function: {function}")

if __name__ == "__main__":
    main()
