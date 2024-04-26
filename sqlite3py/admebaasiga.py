from sqlite3 import *
from sqlite3 import Error, Connection
from os import *


def generate_create_query(connection: Connection):
    table_name: str = input("Tabel name: ")
    print(table_name)
    while True:
        try:
            columns_count: int = int(input("How many columns: "))
            break
        except:
            print("Vale")
    
    column_names: list = list()
    primary_key_column = -1

    for i in enumerate(range(0, columns_count)):
        column_name = input(f"Name of {i[0] + 1} column: ")
        column_type = input(f"Type of {column_name}: ")
        if primary_key_column == -1:
            answer = input(f"{column_name} is primary key? (y/n) \n- ")
            if answer == 'y':
                primary_key_column = i[0] 
        column_names.append([column_name, column_type])
    print(column_names)
    temp_str = str()
    for index, column in enumerate(column_names):
        temp_str += f"{column[0]} {column[1]}{' primary key' if primary_key_column == index else ''} {', ' if index + 1 != len(column_names) else ''}"
    query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({temp_str});"""
    print(query)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except:
        print("Vale, proovi uuesti")
    connection.commit()

def create_connection(path:str):
    connection = None
    try:
        connection = connect(path)
        print("Üheendus on olemas!")
        return connection
    except Error as e:
        print(f"Tekkis viga: {e}")

def close_connection(connection: Connection):
    connection.close()

def execute_query(connection: Connection, query: str):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Tabel on loodud")
    except Error as e:
        print(f"Tekkis viga: {e}")
def execute_read_query(connection: Connection, query: str):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Tekkis viga: {e}")

def execute_insert_query(connection: Connection, data: list, variant: int, tabel:str, ignore:list):
    all_cursor = connection.cursor()
    all_cursor.execute(f"SELECT * FROM {tabel}")
    temp_list = list()
    for i in all_cursor.description:
        if i[0] not in ignore:
            temp_list.append(i[0])
    columns = str()
    for index, i in enumerate(temp_list):
        columns += f"{i}{',' if len(temp_list) != index + 1 else ''}"
    query = f"""
    INSERT INTO {tabel}({columns}) VALUES ({'?' if len(temp_list) == 1 else '?,' * (len(temp_list) - 1) + '?'})
    """
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()

def dropTable(connection: Connection, tabel:str) -> None:
    cursor = connection.cursor()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {tabel}") 
        connection.commit()
    except Error as e:
        print(f"Viga, nagu {e}")

def execute_update_query(connection: Connection, tabel, column, id, value):
    cursor = connection.cursor()
    try:
        cursor.execute(f"UPDATE {tabel} SET {column} = {value} WHERE rowid like {id}") 
        connection.commit()
    except Error as e:
        print(f"Viga, nagu {e}")

create_status_table = """
   CREATE TABLE IF NOT EXISTS status(
   Id INTEGER PRIMARY KEY AUTOINCREMENT,
   Status TEXT 
   )
"""
create_user_table = """
    CREATE TABLE IF NOT EXISTS users(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Lastname TEXT NOT NULL,
    Age INTEGER NOT NULL,
    Birthday TEXT,
    Created_at TEXT NOT NULL,
    Status_id INTEGER ,
    FOREIGN KEY (Status_id) REFERENCES status(Id)
    );
"""


insert_users = """
   INSERT INTO users(Name, Lastname, Age, Birthday, Created_at, Status_id) VALUES
   ('John', 'Doe', 24, '2000-02-05', '2024-04-16', 1),
   ('Jane', 'Doe', 28, '1996-02-05', '2024-04-16', 2),
   ('Mark', 'Pillar', 20, '2004-02-05', '2024-04-16', 3);
"""

insert_status = """
   INSERT INTO status(Status) VALUES ('Admin'), ('User'), ('Artist');
"""
select_users = "SELECT * from users"
select_users_status = "SELECT users.Name, Lastname, status.Status from users INNER JOIN status on users.Status_id = status.Id"

filename = path.abspath(__file__)
dbdir = filename.rstrip('andmebaasiga.py')
dbpath = path.join(dbdir, "data.db")
conn = create_connection(dbpath)
generate_create_query(conn)
execute_query(conn, create_status_table)
execute_query(conn, insert_status)
execute_query(conn, create_user_table)
execute_query(conn, insert_users)
execute_update_query(conn, tabel = 'users', column = 'Name', id = 2, value = '123')
variant = int(input("Variant: "))
insert_user = ((input("Nimi: "),input("Lastname: "),int(input("Age: ")),input("Birthday: "),input("Created at: "),int(input("Status id: ")))) if variant == 1 else ((input('Status: ')),)

print(insert_user)
execute_insert_query(conn, insert_user, variant, 'users' if variant == 1 else "status", ['Id'])
data = execute_read_query(conn, select_users_status)
print(data)

close_connection(conn)
