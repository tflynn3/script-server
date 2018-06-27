import sqlite3
from pprint import pprint

sqlite_file = r'.\my_db.sqlite'


def init_db():
    try:
        with sqlite3.connect(sqlite_file) as conn:
            c = conn.cursor()
            c.execute('CREATE TABLE COMMANDS (ID INTEGER PRIMARY KEY)')
            c.execute("ALTER TABLE COMMANDS ADD COLUMN 'PROCESS' TEXT")
            c.execute("ALTER TABLE COMMANDS ADD COLUMN 'COMMAND' TEXT")
            c.execute("ALTER TABLE COMMANDS ADD COLUMN 'COMPLETED' INTEGER")
            c.execute("ALTER TABLE COMMANDS ADD COLUMN 'RESULT' TEXT")
            conn.commit()
    except Exception as e:
        print(e)


def insert_commands(commands):

    for com in commands:

        id = com['id']
        process = com['process']
        command = com['command']
        completed = com['completed']

        try:
            with sqlite3.connect(sqlite_file) as conn:
                c = conn.cursor()
                print("Running query: INSERT INTO COMMANDS (ID, PROCESS, COMMAND, COMPLETED) VALUES ({}, '{}', '{}', {})".format(id, process, command, completed))
                c.execute("INSERT INTO COMMANDS (ID, PROCESS, COMMAND, COMPLETED) VALUES ({}, '{}', '{}', {})".format(id, process, command, completed))
                conn.commit()
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column ID')


commands = [{
    'id': 1,
    'process': 'powershell.exe',
    'command': 'echo hi',
    'completed': 0
},
{
    'id': 2,
    'process': 'powershell.exe',
    'command': 'Get-Service *win*',
    'completed': 0
}]


def get_commands():
    with sqlite3.connect(sqlite_file) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM COMMANDS')
        all_rows = c.fetchall()
        data = []
        for row in all_rows:
            row_data = {}
            row_data['id'] = row[0]
            row_data['process'] = row[1]
            row_data['command'] = row[2]
            row_data['completed'] = row[3]
            row_data['result'] = row[4]
            data.append(row_data)
    return(data)


def complete_command(id, result=None):
    with sqlite3.connect(sqlite_file) as conn:
        c = conn.cursor()
        c.execute("UPDATE COMMANDS SET COMPLETED=(1) WHERE ID=({})".format(id))
        if result:
            c.execute("UPDATE COMMANDS SET RESULT=('{}') WHERE ID=({})".format(result, id))
        conn.commit()

def get_command(id):
    with sqlite3.connect(sqlite_file) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM COMMANDS WHERE ID=({})'.format(id))


if __name__ == '__main__':
    with sqlite3.connect(sqlite_file) as conn:
        c = conn.cursor()
        init_db()
        insert_commands(commands)
        pprint(get_commands())
        complete_command(1)
        get_commands()
        conn.commit()
