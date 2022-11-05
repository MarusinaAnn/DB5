import psycopg2
from pprint import pprint

def createdb(cur):
    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(30),
        surname VARCHAR (50),
        email VARCHAR(150)
        );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mobilenumbers(
        number VARCHAR(11) PRIMARY KEY,
        clientid INTEGER REFERENCES clients(id)
        );
    """)
    return

def add_number(cur, numb):
    print('Add number command in progress...')
    clientid = int(input('Enter the client id: '))
    cur.execute("""
        INSERT INTO mobilenumbers(number, clientid)
        VALUES (%s, %s)
        """, (numb, clientid))
    return clientid

def add_new_client(cur):
    print('Add the new client command in progress...')
    name = input('Enter the name of client: ')
    surname = input('Enter the surname of client: ')
    email = input('Enter the email of client: ')
    cur.execute("""
        INSERT INTO clients(name, surname, email)
        VALUES (%s, %s, %s)
        """, (name, surname, email))
    cur.execute("""
        SELECT id from clients
        ORDER BY id DESC
        LIMIT 1
        """)
    id = cur.fetchone()[0]
    number_access = input('Do you want to add phone number? (y/n): ').lower()
    if number_access == 'y':
        numb = input('Enter the number: ')
        print(f'Client id is {id}')
        add_number(cur, numb)
        return id
    else: 
        return id

    
def update_info(cur):
    print('Update command in progress...')
    print('Available commands: /n1 - search by name, 2 - search by surname, 3 - search by email, 4 - search by phonenumber') 
    cs = int(input('Please,enter command: '))
    while True:
        if cs == 1:
            past_name_id = input("Enter the id of the client whose name you want to change: ")
            new_name = input("Enter new name: ")
            cur.execute("""
            UPDATE clients SET name=%s WHERE id=%s;
            """, (new_name, past_name_id))
            break
        elif cs == 2:
            past_surname_id = input("Enter the id of the client whose surname you want to change: ")
            new_surname = input("Enter new surname: ")
            cur.execute("""
            UPDATE clients SET surname=%s WHERE id=%s;
            """, (new_surname, past_surname_id))
            break
        elif cs == 3:
            past_email_id = input("Enter the id of the client whose email you want to change: ")
            new_email = input("Enter new email: ")
            cur.execute("""
            UPDATE clients SET email=%s WHERE id=%s;
            """, (new_email, past_email_id))
            break
        elif cs == 4:
            past_number = input("Enter the number that you want to change: ")
            new_number = input("Enter new number: ")
            cur.execute("""
            UPDATE mobilenumbers SET number=%s WHERE number=%s;
            """, (new_number, past_number))
            break
        else:
            print("Wrong command")


def drop_number(cur):
    print('Delete phonenumber command in progress...')
    past_number_id = input("Enter the id of the client whose number you want to delete: ")
    past_number_del = input("Enter the number that you want to delete: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM mobilenumbers WHERE clientid=%s AND number=%s
        """, (past_number_id, past_number_del))  

def drop_client(cur):
    print('Delete client command in progress...')
    id = int(input('Enter the id of client: '))
    cur.execute("""
        DELETE FROM mobilenumbers
        WHERE client_id = %s
        """, (id, ))
    cur.execute("""
        DELETE FROM clients 
        WHERE id = %s
       """, (id,))
    return id 


def search_client(cur, name=None, surname=None, email=None, tel=None):
    print('Search client command in progress...')
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if surname is None:
        surname = '%'
    else:
        surname = '%' + surname + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if tel is None:
        cur.execute("""
            SELECT c.id, c.name, c.surname, c.email, p.number FROM clients c
            LEFT JOIN mobilenumbers m ON c.id = m.clientid
            WHERE c.name LIKE %s AND c.surname LIKE %s
            AND c.email LIKE %s
            """, (name, surname, email))
    else:
        cur.execute("""
            SELECT c.id, c.name, c.surname, c.email, p.number FROM clients c
            LEFT JOIN mobilenumbers m ON c.id = m.client_id
            WHERE c.name LIKE %s AND c.surname LIKE %s
            AND c.email LIKE %s AND m.number like %s
            """, (name, surname, email, tel))
    return cur.fetchall()

def check(cur):
    cur.execute("""
    SELECT * FROM clients;
    """)
    pprint(cur.fetchall())
    cur.execute("""
    SELECT * FROM mobilenumbers;
    """)
    pprint(cur.fetchall())

def deletedb(cur):
    cur.execute("""
        DROP TABLE clients, mobilenumbers CASCADE;
        """)



if __name__ == '__main__':
    conn = psycopg2.connect(database='hwdb5', user='postgres',password='644882')
    with conn.cursor() as cur:
        deletedb(cur)
        createdb(cur)
        add_new_client(cur)
        check(cur)
        add_new_client(cur)
        check(cur)
        add_number(cur, 88065678392)
        check(cur)
        update_info(cur)
        check(cur)
        drop_number(cur)
        check(cur)
        
        conn.commit()
    conn.close()