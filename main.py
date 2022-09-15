import psycopg2
from pprint import pprint

def create_db(conn):

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(80) UNIQUE,
        last_name VARCHAR(80) UNIQUE,
        email VARCHAR(80)
        );
        """)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_numbers(
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(20),
        client_id INTEGER NOT NULL REFERENCES clients(id)
        );
        """)

def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO clients(first_name, last_name, email)
        VALUES (%s, %s, %s)
        """, (first_name, last_name, email))
        print(f'Клиент {first_name} {last_name} добавлен в базу данных')

def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone_numbers(client_id, phone_number)
        VALUES (%s, %s)
        """, (client_id, phone_number))
        print(f'Телефон добавлен в базу данных')

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone_number=None):
    while True:
        command = int(input(
            'Введите команду для изменения данных:'
            '\n1 - Изменить имя,'
            '\n2 - изменить фамилию,'
            '\n3 - изменить email,'
            '\n4 - изменить номер телефона\n'))
        changing_client_id = input('Введите id клиента')

        if command == 1:
            new_client_name = input('Введите новое имя')
            with conn.cursor() as cur:
                cur.execute("""
            UPDATE clients SET first_name = %s WHERE id = %s;
            """, (new_client_name, changing_client_id))
            break

        elif command == 2:
            new_client_surname = input('Введите новую фамилию')
            with conn.cursor() as cur:
                cur.execute("""
            UPDATE clients SET last_name = %s WHERE id = %s;
            """, (new_client_surname, changing_client_id))
            break

        elif command == 3:
            new_client_email = input('Введите email')
            with conn.cursor() as cur:
                cur.execute("""
            UPDATE clients SET last_name = %s WHERE id = %s;
            """, (new_client_email, changing_client_id))
            break

        elif command == 4:
            changing_phone = input('Введите номер, который хотите изменить')
            new_phone = input('Введите новый номер')
            with conn.cursor() as cur:
                cur.execute("""
            UPDATE phone_numbers SET phone_number = %s WHERE phone_number = %s;
            """, (new_phone, changing_phone))
            break

def delete_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
    DELETE  FROM phone_numbers WHERE client_id = %s AND phone_number=%s;
    """, (client_id, phone_number))
        print(f'Номер телефона удален из базы данных')

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
    DELETE  FROM phone_numbers WHERE client_id = %s;
    """, (client_id,))
    with conn.cursor() as cur:
        cur.execute("""
    DELETE  FROM clients WHERE id = %s;
    """, (client_id,))
        print(f'Данные клиента удалены из базы данных')

def find_client(conn, first_name=None, last_name=None, email=None, phone_number=None):
    while True:
        command_1 = int(input(
            'Введите команду для поиска данных:'
            '\n1 - по имени,'
            '\n2 - по фамилии,'
            '\n3 - по email,'
            '\n4 - по номеру телефона\n'))

        if command_1 == 1:
            finding_client_name = input('Введите имя: ')
            with conn.cursor() as cur:
                cur.execute("""
            SELECT first_name, last_name, email, phone_number FROM clients c
            JOIN phone_numbers p ON p.client_id = c.id
            WHERE first_name = %s
            """, (finding_client_name,))
                print(cur.fetchall())
                break

        elif command_1 == 2:
            finding_client_surname = input('Введите фамилию: ')
            with conn.cursor() as cur:
                cur.execute("""
            SELECT first_name, last_name, email, phone_number FROM clients c
            JOIN phone_numbers p ON p.client_id = c.id
            WHERE last_name = %s
            """, (finding_client_surname,))
                print(cur.fetchall())
                break

        elif command_1 == 3:
            finding_client_email = input('Введите email: ')
            with conn.cursor() as cur:
                cur.execute("""
            SELECT first_name, last_name, email, phone_number FROM clients c
            LEFT JOIN phone_numbers p ON p.client_id = c.id
            WHERE email = %s
            """, (finding_client_email,))
                print(cur.fetchall())
                break

        elif command_1 == 4:
            finding_phone = input('Введите номер телефона: ')
            with conn.cursor() as cur:
                cur.execute("""
            SELECT first_name, last_name, email, phone_number FROM clients c
            LEFT JOIN phone_numbers p ON p.client_id = c.id
            WHERE phone_number = %s
            """, (finding_phone,))
                print(cur.fetchall())
                break

def select_function(conn):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM clients;
        """)
        pprint(cur.fetchall())
        cur.execute("""
        SELECT * FROM phone_numbers;
        """)
        pprint(cur.fetchall())

with psycopg2.connect(database="clients_db", user="postgres", password="") as conn:
    create_db(conn)
    add_client(conn, 'Иван', 'Иванов', 'ivanov@email.ru')
    add_client(conn, 'Петр', 'Сидоров', 'psidorov@email.ru')
    add_client(conn, 'Анна', 'Петрова', 'petrovaanna@email.ru')
    add_client(conn, 'Ольга', 'Краснова', 'krasnova@email.ru')
    add_phone(conn, 1, '+79876543210')
    add_phone(conn, 1, '+79123456789')
    add_phone(conn, 2, '+79321654987')
    add_phone(conn, 3, '+79014785236')
    add_phone(conn, 4, '+79234567890')
    change_client(conn, client_id=None)
    delete_phone(conn, 2, '+79321654987')
    delete_client(conn, 4)
    find_client(conn, first_name=None, last_name=None, email=None, phone_number=None)
    select_function(conn)

conn.close()
