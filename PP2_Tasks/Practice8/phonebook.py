import psycopg2
from connect import get_connection


def search_by_pattern():
    pattern = input("Enter search pattern: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts_by_pattern(%s);", (pattern,))
        rows = cur.fetchall()

        if rows:
            print("\nMatched contacts:")
            for row in rows:
                print(row)
        else:
            print("No contacts found.")
    except Exception as e:
        print("Error while searching:", e)
    finally:
        cur.close()
        conn.close()


def get_paginated_contacts():
    limit_value = int(input("Enter limit: ").strip())
    offset_value = int(input("Enter offset: ").strip())

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s);",
            (limit_value, offset_value)
        )
        rows = cur.fetchall()

        if rows:
            print("\nPaginated contacts:")
            for row in rows:
                print(row)
        else:
            print("No contacts found.")
    except Exception as e:
        print("Error while pagination query:", e)
    finally:
        cur.close()
        conn.close()


def upsert_one_contact():
    first_name = input("Enter first name: ").strip()
    surname = input("Enter surname: ").strip()
    phone = input("Enter phone: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "CALL upsert_contact(%s, %s, %s);",
            (first_name, surname, phone)
        )
        conn.commit()
        print("Upsert completed.")
    except Exception as e:
        conn.rollback()
        print("Error while upsert:", e)
    finally:
        cur.close()
        conn.close()


def insert_many_contacts():
    print("How many contacts do you want to insert?")
    n = int(input().strip())

    first_names = []
    surnames = []
    phones = []

    for i in range(n):
        print(f"\nContact {i+1}")
        first_names.append(input("First name: ").strip())
        surnames.append(input("Surname: ").strip())
        phones.append(input("Phone: ").strip())

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "CALL insert_many_contacts(%s, %s, %s);",
            (first_names, surnames, phones)
        )
        conn.commit()
        print("Bulk insert completed. Check notices for incorrect data.")
    except Exception as e:
        conn.rollback()
        print("Error while bulk insert:", e)
    finally:
        cur.close()
        conn.close()


def delete_contact():
    print("1. Delete by first name")
    print("2. Delete by phone")
    choice = input("Choose option: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        if choice == "1":
            first_name = input("Enter first name: ").strip()
            cur.execute("CALL delete_contact_proc(%s, %s);", (first_name, None))
        elif choice == "2":
            phone = input("Enter phone: ").strip()
            cur.execute("CALL delete_contact_proc(%s, %s);", (None, phone))
        else:
            print("Invalid choice.")
            return

        conn.commit()
        print("Delete completed.")
    except Exception as e:
        conn.rollback()
        print("Error while deleting:", e)
    finally:
        cur.close()
        conn.close()


def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, first_name, surname, phone FROM phonebook ORDER BY id;"
        )
        rows = cur.fetchall()

        if rows:
            print("\nAll contacts:")
            for row in rows:
                print(row)
        else:
            print("Phonebook is empty.")
    except Exception as e:
        print("Error while reading contacts:", e)
    finally:
        cur.close()
        conn.close()


def menu():
    while True:
        print("\n--- PRACTICE 8 PHONEBOOK MENU ---")
        print("1. Search contacts by pattern")
        print("2. Upsert one contact")
        print("3. Insert many contacts")
        print("4. Get contacts with pagination")
        print("5. Delete contact")
        print("6. Show all contacts")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_by_pattern()
        elif choice == "2":
            upsert_one_contact()
        elif choice == "3":
            insert_many_contacts()
        elif choice == "4":
            get_paginated_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            show_all_contacts()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()