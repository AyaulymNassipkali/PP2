import psycopg2
from tabulate import tabulate

conn = psycopg2.connect(
    host="localhost",
    dbname="phonebook_db",
    user="postgres",
    password="12345678",
    port=5432
)

delete_by_name_or_phone = '''CREATE OR REPLACE PROCEDURE public.delete_by_name_or_phone(IN p_value text)
  LANGUAGE plpgsql
AS $procedure$
BEGIN
    DELETE FROM phonebook WHERE name = p_value OR phone = p_value;
END;
$procedure$
'''

get_paginated = '''CREATE OR REPLACE FUNCTION public.get_paginated(limit_value integer, offset_value integer)
  RETURNS TABLE(id integer, name character varying, surname character varying, phone character varying)
  LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT phonebook.id, phonebook.name, phonebook.surname, phonebook.phone
    FROM phonebook
    ORDER BY phonebook.id
    LIMIT limit_value OFFSET offset_value;
END;
$function$
'''

get_paginated_users = '''CREATE OR REPLACE FUNCTION public.get_paginated_users(p_limit integer, p_offset integer)
  RETURNS TABLE(user_id integer, name text, surname text, phone text)
  LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT phonebook.user_id, phonebook.name, phonebook.surname, phonebook.phone
    FROM phonebook
    ORDER BY phonebook.user_id
    LIMIT p_limit OFFSET p_offset;
END;
$function$
'''

insert_many_users_return_invalid = '''CREATE OR REPLACE FUNCTION public.insert_many_users_return_invalid(names text[], phones text[])
  RETURNS TABLE(invalid_name text, invalid_phone text)
  LANGUAGE plpgsql
AS $function$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF names[i] IS NULL OR phones[i] IS NULL OR phones[i] !~ '^\+?\d{10,15}$' THEN
            -- возвращаем как некорректные
            RETURN QUERY SELECT names[i], phones[i];
        END IF;
    END LOOP;
    RETURN;
END;
$function$
'''

insert_many_users_return_invalid = '''CREATE OR REPLACE FUNCTION public.insert_many_users_return_invalid(names text[], surnames text[], phones text[])
  RETURNS TABLE(name text, surname text, phone text)
  LANGUAGE plpgsql
AS $function$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF phones[i] ~ '^\d{11}$' THEN
            INSERT INTO phonebook(name, surname, phone)
            VALUES (names[i], surnames[i], phones[i]);
        ELSE
            -- если телефон не соответствует формату, возвращаем его как некорректный
            RETURN QUERY SELECT names[i], surnames[i], phones[i];
        END IF;
    END LOOP;
    RETURN;
END;
$function$
'''

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
    surnames = []
    phones = []
    for _ in range(n):
        names.append(input("Name: "))
        surnames.append(input("Surnames: "))
        phones.append(input("Phone: "))
    cur.execute("SELECT * FROM insert_many_users_return_invalid(%s, %s, %s);", (names, surnames, phones))
    invalid_rows = cur.fetchall()
    if invalid_rows:
        print("❌ Invalid rows:")
        for row in invalid_rows:
            print(f"Name: {row[0]}, Surname: {row[1]}, Phone: {row[2]}")
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

