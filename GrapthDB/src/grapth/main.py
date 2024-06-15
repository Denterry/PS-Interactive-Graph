from neo4j import GraphDatabase

# Код для подключения
class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def query(self, query, db=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", password="adminadmin")

conn.query("CREATE OR REPLACE DATABASE graphdb")
query_string = '''
CREATE (student1:Student {name: "Student 1"}),
  (student2:Student {name: "Student 2"}),
  (student3:Student {name: "Student 3"}),
  (student4:Student {name: "Student 4"}),
  (student5:Student {name: "Student 5"}),
  (student6:Student {name: "Student 6"}),
  (professor1:Professor {name: "Professor 1"}),
  (professor2:Professor {name: "Professor 2"}),
  (professor3:Professor {name: "Professor 3"}),
  (group1:Group {name: "Group 1", student_number: 20}),
  (group2:Group {name: "Group 2", student_number: 25}),
  (group3:Group {name: "Group 3", student_number: 30}),
  (mathematics:Discipline {name: "Mathematics"}),
  (physics:Discipline {name: "Physics"}),
  (chemistry:Discipline {name: "Chemistry"}),
  (lesson1:Lesson {id: 1, start_time: "09:00", duration_time: 90, max_students: 30}),
  (lesson2:Lesson {id: 2, start_time: "11:00", duration_time: 90, max_students: 25}),
  (lesson3:Lesson {id: 3, start_time: "13:00", duration_time: 90, max_students: 20}),

  (lesson1)-[:PART_OF]->(mathematics),
  (lesson2)-[:PART_OF]->(physics),
  (lesson3)-[:PART_OF]->(chemistry),

  (lesson1)-[:ATTENDED_BY]->(group1),
  (lesson2)-[:ATTENDED_BY]->(group2),
  (lesson3)-[:ATTENDED_BY]->(group3),

  (lesson1)-[:TAUGHT_BY]->(professor1),
  (lesson2)-[:TAUGHT_BY]->(professor2),
  (lesson3)-[:TAUGHT_BY]->(professor3),

  (student1)-[:BELONGS_TO]->(group1),
  (student2)-[:BELONGS_TO]->(group1),
  (student3)-[:BELONGS_TO]->(group2),
  (student4)-[:BELONGS_TO]->(group2),
  (student5)-[:BELONGS_TO]->(group3),
  (student6)-[:BELONGS_TO]->(group3)
'''
conn.query(query_string)

conn.close()
