import psycopg2
from tabulate import tabulate

conn = psycopg2.connect(
    host="localhost",
    dbname="phonebook_db",
    user="postgres",
    password="12345678",
    port=5432
)

cur = conn.cursor()

def search_by_pattern():
    pattern = input("Enter pattern (part of name/surname/phone): ")
    cur.execute("SELECT * FROM search_pattern(%s);", (pattern,))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))

def insert_or_update():
    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone: ")
    cur.execute("CALL insert_or_update_user(%s, %s, %s);", (name, surname, phone))
    conn.commit()
    print("✅ Inserted or updated successfully.")

def insert_many():
    n = int(input("How many users to insert? "))
    names = []
    phones = []
    for _ in range(n):
        names.append(input("Name: "))
        phones.append(input("Phone: "))
    cur.execute("SELECT * FROM insert_many_users_return_invalid(%s, %s);", (names, phones))
    invalid_rows = cur.fetchall()
    if invalid_rows:
        print("❌ Invalid rows:")
        for row in invalid_rows:
            print(f"Name: {row[0]}, Phone: {row[1]}")
    else:
        print("✅ All users inserted successfully.")
    conn.commit()

def paginated_query():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))
    cur.execute("SELECT * FROM get_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))

def show_all_users():
    cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))

def delete_by_value():
    value = input("Enter name or phone to delete: ")
    cur.execute("CALL delete_by_name_or_phone(%s);", (value,))
    conn.commit()
    print("🗑️ Entry deleted (if existed).")

while True:
    print("""
    PostgreSQL PhoneBook - Lab 11
    1. Search by pattern
    2. Insert or update user
    3. Insert many users (with validation)
    4. Get paginated users
    5. Delete by name or phone
    6. Show all users
    7. Exit
    """)

    cmd = input("Choose option (1-7): ")

    if cmd == "1":
        search_by_pattern()
    elif cmd == "2":
        insert_or_update()
    elif cmd == "3":
        insert_many()
    elif cmd == "4":
        paginated_query()
    elif cmd == "5":
        delete_by_value()
    elif cmd == "6":
        show_all_users()
    elif cmd == "7":
        break
    else:
        print("Invalid command")

cur.close()
conn.close()
