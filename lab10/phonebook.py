import psycopg2
import csv
from tabulate import tabulate

conn = psycopg2.connect(
    host = "localhost", dbname = "lab10", user = "postgres",
    password = "12345678", port = 5432
)

cur = conn.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL
            )
""")
conn.commit()

def insert_console():
    name = input("Name: ")
    surname = input("Surname: ")
    phone = input("Phone: ")
    cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
    conn.commit()



def insert_csv():
    path = input("Enter CSV file path: ")
    with open(path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", tuple(row))
    conn.commit()



def update_column(column):
    old_value = input(f"Enter current {column}: ")
    new_value = input(f"Enter new {column}: ")
    cur.execute(f"UPDATE phonebook SET {column} = %s WHERE {column} = %s", (new_value, old_value))
    conn.commit



def delete_by_phone():
    phone = input("Enter phone to delete: ")
    cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()

def query_by_column(column):
    value = input(f"Enter {column}: ")
    if column == "id":  # Обработка запроса по ID
        column = "user_id"
    cur.execute(f"SELECT * FROM phonebook WHERE {column} = %s", (value,))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))

def show_all():
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    print(tabulate(rows, headers = ["ID", "Name", "Surname", "Phone"], tablefmt="fancy_grid"))


def menu():
    while True:
        print("""
        === MENU ===
        [i] Insert (console ot csv)
        [u] Update
        [d] Delete
        [q] Query
        [s] Show all
        [f] Finish
        """)
        
        cmd = input("Choose command: ").lower()

        if cmd == "i":
            opt = input('Type "csv" to upload file or "con" to enter manually: ')
            if opt == "con": insert_console()
            elif opt == "csv": insert_csv()

        elif cmd == "u":
            col = input("Which column to update (name/surname/phone): ")
            if col in ["name", "surname", "phone"]:
                update_column(col)

        elif cmd == "d":
            delete_by_phone()

        elif cmd == "q":
            col = input("Search by (id/name/surname/phone): ")
            if col in ["id", "name", "surname", "phone"]:
                query_by_column(col)

        elif cmd == "s":
            show_all()

        elif cmd == "f":
            break

menu()

cur.close()
conn.close()

