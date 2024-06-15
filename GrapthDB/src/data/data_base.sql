CREATE TABLE Group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    student_number INTEGER NOT NULL
);

CREATE TABLE Student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    group_id INTEGER NOT NULL,
    lesson_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES Groupp(id),
    FOREIGN KEY (lesson_id) REFERENCES Lesson(id)
);

CREATE TABLE Professor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    discipline_id INTEGER,
    FOREIGN KEY (discipline_id) REFERENCES Discipline(id)
);

CREATE TABLE Discipline (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Lesson (
    id SERIAL PRIMARY KEY,
    start_time TIME NOT NULL,
    duration_time INTEGER NOT NULL,
    max_students INTEGER NOT NULL,
    discipline_id INTEGER,
    professor_id INTEGER,
    FOREIGN KEY (discipline_id) REFERENCES Discipline(id),
    FOREIGN KEY (professor_id) REFERENCES Pprofessor(id)
);
