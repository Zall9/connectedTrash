import sqlite3
import os.path

def createDbConnection() -> sqlite3.Connection:
    path = "database.db"
    check_file = os.path.isfile(path)
    con = sqlite3.connect(path)
    if not check_file:
        seedDb(con)
    return con

def seedDb(con):
    con.execute("CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY, name VARCHAR(100));")
    
    con.execute("INSERT INTO user (name) VALUES ('Mathis Tangue');")
    con.execute("INSERT INTO user (name) VALUES ('Christophe Courtin');")

    con.execute("CREATE TABLE IF NOT EXISTS response (id INTEGER PRIMARY KEY, user_id INTEGER, answer BOOLEAN, user_response BOOLEAN);")
    con.execute("INSERT INTO response (user_id, answer, user_response) VALUES (2, 0, 1);")
    con.execute("INSERT INTO response (user_id, answer, user_response) VALUES (2, 1, 1);")
    con.commit()

class User:
    @staticmethod
    def findOne(id):
        con = createDbConnection()
        res = con.execute(f'SELECT * from user WHERE id = \'{id}\'')
        return res.fetchone()

    @staticmethod
    def findAll():
        con = createDbConnection()
        res = con.execute("SELECT * from user")
        return res.fetchall()

class Response:
    @staticmethod
    def findByUser(user_id):
        con = createDbConnection()
        res = con.execute(f'SELECT * from response WHERE user_id = \'{user_id}\'')
        return res.fetchall()
    
    @staticmethod
    def createResponse(user_id, answer, user_response):
        con = createDbConnection()
        con.execute(f'INSERT INTO response (user_id, answer, user_response) VALUES ({user_id}, {answer}, {user_response});')
        con.commit()
        con.close()

    @staticmethod
    def getLastUserResponse(user_id):
        con = createDbConnection()
        res = con.execute(f'SELECT * FROM response WHERE user_id = {user_id} ORDER BY ID DESC LIMIT 1')
        return res.fetchone()