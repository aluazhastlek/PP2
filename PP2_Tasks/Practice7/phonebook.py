import csv
from connect import get_connection

#creating table
def create_table():
    query= """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    );
    """
    conn=get_connection()
    cur=conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
        print("Table created successfully")
    except Exception as e:
        conn.rollback()
        print("Error while creating table:", e)
    finally:
        cur.close()
        conn.close()

#inserting contact into a table
def insert_from_console():
    first_name=input("Enter name: ").strip()
    phone=input("Enter phonenumber: ").strip()

    query="""
    INSERT INTO phonebook (first_name, phone)
    VALUES (%s,%s)
    """
    conn=get_connection()
    cur=conn.cursor()
    try:
        cur.execute(query, (first_name, phone))
        conn.commit()
        print("Contact added succesfully")
    except Exception as e:
        conn.rollback()
        print("Error while inserting contact: ", e)
    finally:
        cur.close()
        conn.close()

#inserting contact into a table from csv
def insert_from_csv(filename="contacts.csv"):
    query = """
    INSERT INTO phonebook (first_name, phone)
    VALUES (%s, %s)
    ON CONFLICT (phone) DO NOTHING;
    """

    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  
            for row in reader:
                if len(row) >= 2:
                    first_name, phone = row[0].strip(), row[1].strip()
                    cur.execute(query, (first_name, phone))

        conn.commit()
        print("CSV data imported successfully.")
    except Exception as e:
        conn.rollback()
        print("Error while importing CSV:", e)
    finally:
        cur.close()
        conn.close()

#to see all contacts from DB
def show_all_contacts():
    query = "SELECT * FROM phonebook ORDER BY id;"

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()

        if not rows:
            print("PhoneBook is empty.")
        else:
            print("\nContacts:")
            for row in rows:
                print(row)
    except Exception as e:
        print("Error while reading contacts:", e)
    finally:
        cur.close()
        conn.close()


#searching contact by name
def search_by_name():
    name = input("Enter name to search: ").strip()

    query = """
    SELECT * FROM phonebook
    WHERE first_name ILIKE %s;
    """

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, (f"%{name}%",))
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts found.")
    except Exception as e:
        print("Error while searching by name:", e)
    finally:
        cur.close()
        conn.close()


#searching contact by phone
def search_by_phone_prefix():
    prefix = input("Enter phone prefix: ").strip()

    query = """
    SELECT * FROM phonebook
    WHERE phone LIKE %s;
    """

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, (f"{prefix}%",))
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts found.")
    except Exception as e:
        print("Error while searching by prefix:", e)
    finally:
        cur.close()
        conn.close()

#changinging contact's name/phone
def update_contact():
    print("1. Update name by phone")
    print("2. Update phone by name")
    choice = input("Choose option: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            phone = input("Enter current phone: ").strip()
            new_name = input("Enter new name: ").strip()

            query = """
            UPDATE phonebook
            SET first_name = %s
            WHERE phone = %s;
            """
            cur.execute(query, (new_name, phone))

        elif choice == "2":
            name = input("Enter current name: ").strip()
            new_phone = input("Enter new phone: ").strip()

            query = """
            UPDATE phonebook
            SET phone = %s
            WHERE first_name = %s;
            """
            cur.execute(query, (new_phone, name))

        else:
            print("Invalid choice.")
            return

        conn.commit()

        if cur.rowcount == 0:
            print("No contact found to update.")
        else:
            print("Contact updated successfully.")

    except Exception as e:
        conn.rollback()
        print("Error while updating contact:", e)
    finally:
        cur.close()
        conn.close()


#deleting contact's information by name/phone
def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")
    choice = input("Choose option: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            name = input("Enter name to delete: ").strip()
            query = "DELETE FROM phonebook WHERE first_name = %s;"
            cur.execute(query, (name,))

        elif choice == "2":
            phone = input("Enter phone to delete: ").strip()
            query = "DELETE FROM phonebook WHERE phone = %s;"
            cur.execute(query, (phone,))

        else:
            print("Invalid choice.")
            return

        conn.commit()

        if cur.rowcount == 0:
            print("No contact found to delete.")
        else:
            print("Contact deleted successfully.")

    except Exception as e:
        conn.rollback()
        print("Error while deleting contact:", e)
    finally:
        cur.close()
        conn.close()


#menu of program to process the DB
def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert contact from console")
        print("3. Import contacts from CSV")
        print("4. Show all contacts")
        print("5. Search by name")
        print("6. Search by phone prefix")
        print("7. Update contact")
        print("8. Delete contact")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            insert_from_csv()
        elif choice == "4":
            show_all_contacts()
        elif choice == "5":
            search_by_name()
        elif choice == "6":
            search_by_phone_prefix()
        elif choice == "7":
            update_contact()
        elif choice == "8":
            delete_contact()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()