import csv
import json
from connect import get_connection


def execute_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            cur.execute(file.read())
        conn.commit()
        print(f"{filename} executed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error while executing {filename}:", e)
    finally:
        cur.close()
        conn.close()


def setup_database():
    execute_sql_file("schema.sql")
    execute_sql_file("procedures.sql")


def get_group_id(cur, group_name):
    if not group_name:
        group_name = "Other"

    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (group_name,)
    )
    cur.execute("SELECT id FROM groups WHERE LOWER(name) = LOWER(%s);", (group_name,))
    return cur.fetchone()[0]


def find_contact_id(cur, first_name, surname=None):
    if surname:
        cur.execute(
            """
            SELECT id FROM contacts
            WHERE LOWER(first_name) = LOWER(%s)
            AND LOWER(COALESCE(surname, '')) = LOWER(%s)
            LIMIT 1;
            """,
            (first_name, surname)
        )
    else:
        cur.execute(
            "SELECT id FROM contacts WHERE LOWER(first_name) = LOWER(%s) LIMIT 1;",
            (first_name,)
        )
    row = cur.fetchone()
    return row[0] if row else None


def add_contact_interactive():
    first_name = input("First name: ").strip()
    surname = input("Surname: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday (YYYY-MM-DD or empty): ").strip() or None
    group_name = input("Group (Family/Work/Friend/Other): ").strip() or "Other"
    phone = input("Phone: ").strip()
    phone_type = input("Phone type (home/work/mobile): ").strip().lower() or "mobile"

    conn = get_connection()
    cur = conn.cursor()
    try:
        group_id = get_group_id(cur, group_name)
        cur.execute(
            """
            INSERT INTO contacts (first_name, surname, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (first_name, surname, email, birthday, group_id)
        )
        contact_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
            (contact_id, phone, phone_type)
        )
        conn.commit()
        print("Contact added successfully.")
    except Exception as e:
        conn.rollback()
        print("Error while adding contact:", e)
    finally:
        cur.close()
        conn.close()


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print("-" * 70)
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]} {row[2] or ''}")
        print(f"Email: {row[3] or ''}")
        print(f"Birthday: {row[4] or ''}")
        print(f"Group: {row[5] or ''}")
        print(f"Phones: {row[6] or ''}")


def show_all_contacts(order_by="id"):
    allowed = {
        "id": "c.id",
        "name": "c.first_name, c.surname",
        "birthday": "c.birthday NULLS LAST",
        "date": "c.created_at DESC"
    }
    order_sql = allowed.get(order_by, allowed["id"])

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT
                c.id,
                c.first_name,
                c.surname,
                c.email,
                c.birthday,
                g.name,
                COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.first_name, c.surname, c.email, c.birthday, g.name, c.created_at
            ORDER BY {order_sql};
        """)
        print_contacts(cur.fetchall())
    except Exception as e:
        print("Error while showing contacts:", e)
    finally:
        cur.close()
        conn.close()


def filter_by_group():
    group_name = input("Enter group name: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT
                c.id, c.first_name, c.surname, c.email, c.birthday, g.name,
                COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE LOWER(g.name) = LOWER(%s)
            GROUP BY c.id, c.first_name, c.surname, c.email, c.birthday, g.name
            ORDER BY c.first_name;
            """,
            (group_name,)
        )
        print_contacts(cur.fetchall())
    except Exception as e:
        print("Error while filtering by group:", e)
    finally:
        cur.close()
        conn.close()


def search_by_email():
    query = input("Enter email search text: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT
                c.id, c.first_name, c.surname, c.email, c.birthday, g.name,
                COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE c.email ILIKE %s
            GROUP BY c.id, c.first_name, c.surname, c.email, c.birthday, g.name
            ORDER BY c.first_name;
            """,
            (f"%{query}%",)
        )
        print_contacts(cur.fetchall())
    except Exception as e:
        print("Error while searching by email:", e)
    finally:
        cur.close()
        conn.close()


def search_all_fields():
    query = input("Search name / surname / email / group / phone: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts(%s);", (query,))
        print_contacts(cur.fetchall())
    except Exception as e:
        print("Error while searching all fields:", e)
    finally:
        cur.close()
        conn.close()


def sort_contacts_menu():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")
    choice = input("Choose: ").strip()

    if choice == "1":
        show_all_contacts("name")
    elif choice == "2":
        show_all_contacts("birthday")
    elif choice == "3":
        show_all_contacts("date")
    else:
        print("Invalid choice.")


def paginated_navigation():
    limit = int(input("Page size: ").strip() or "5")
    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
            rows = cur.fetchall()
            print(f"\nPage starting from offset {offset}")
            print_contacts(rows)
        except Exception as e:
            print("Error while paginating:", e)
        finally:
            cur.close()
            conn.close()

        command = input("next / prev / quit: ").strip().lower()
        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Unknown command.")


def add_phone_procedure():
    name = input("Contact first name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Type (home/work/mobile): ").strip().lower()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))
        conn.commit()
        print("Phone added.")
    except Exception as e:
        conn.rollback()
        print("Error while adding phone:", e)
    finally:
        cur.close()
        conn.close()


def move_to_group_procedure():
    name = input("Contact first name: ").strip()
    group_name = input("New group: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s);", (name, group_name))
        conn.commit()
        print("Contact moved to group.")
    except Exception as e:
        conn.rollback()
        print("Error while moving group:", e)
    finally:
        cur.close()
        conn.close()


def export_to_json(filename="contacts.json"):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT c.id, c.first_name, c.surname, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id;
            """
        )
        contacts = []
        for contact_id, first_name, surname, email, birthday, group_name in cur.fetchall():
            cur.execute(
                "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id;",
                (contact_id,)
            )
            phones = [{"phone": phone, "type": phone_type} for phone, phone_type in cur.fetchall()]
            contacts.append({
                "first_name": first_name,
                "surname": surname,
                "email": email,
                "birthday": birthday.isoformat() if birthday else None,
                "group": group_name,
                "phones": phones
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4, ensure_ascii=False)
        print(f"Exported to {filename}.")
    except Exception as e:
        print("Error while exporting JSON:", e)
    finally:
        cur.close()
        conn.close()


def insert_contact_from_dict(cur, item, overwrite=False):
    first_name = item.get("first_name", "").strip()
    surname = item.get("surname", "").strip()
    email = item.get("email")
    birthday = item.get("birthday") or None
    group_name = item.get("group") or "Other"
    phones = item.get("phones", [])

    group_id = get_group_id(cur, group_name)
    existing_id = find_contact_id(cur, first_name, surname)

    if existing_id and overwrite:
        cur.execute(
            """
            UPDATE contacts
            SET email = %s, birthday = %s, group_id = %s
            WHERE id = %s;
            """,
            (email, birthday, group_id, existing_id)
        )
        cur.execute("DELETE FROM phones WHERE contact_id = %s;", (existing_id,))
        contact_id = existing_id
    elif existing_id and not overwrite:
        return "skipped"
    else:
        cur.execute(
            """
            INSERT INTO contacts (first_name, surname, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (first_name, surname, email, birthday, group_id)
        )
        contact_id = cur.fetchone()[0]

    for phone_item in phones:
        phone = phone_item.get("phone")
        phone_type = phone_item.get("type", "mobile")
        if phone:
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                (contact_id, phone, phone_type)
            )
    return "inserted"


def import_from_json(filename="contacts.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        print("Error while reading JSON:", e)
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        for item in data:
            first_name = item.get("first_name", "")
            surname = item.get("surname", "")
            existing_id = find_contact_id(cur, first_name, surname)

            overwrite = False
            if existing_id:
                answer = input(f"Duplicate {first_name} {surname}. skip or overwrite? ").strip().lower()
                if answer == "overwrite":
                    overwrite = True
                else:
                    print("Skipped.")
                    continue

            insert_contact_from_dict(cur, item, overwrite)

        conn.commit()
        print("JSON import completed.")
    except Exception as e:
        conn.rollback()
        print("Error while importing JSON:", e)
    finally:
        cur.close()
        conn.close()


def import_from_csv(filename="contacts.csv"):
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                item = {
                    "first_name": row.get("first_name", "").strip(),
                    "surname": row.get("surname", "").strip(),
                    "email": row.get("email", "").strip(),
                    "birthday": row.get("birthday", "").strip() or None,
                    "group": row.get("group", "Other").strip() or "Other",
                    "phones": [
                        {
                            "phone": row.get("phone", "").strip(),
                            "type": row.get("phone_type", "mobile").strip().lower() or "mobile"
                        }
                    ]
                }

                existing_id = find_contact_id(cur, item["first_name"], item["surname"])

                overwrite = False
                if existing_id:
                    answer = input(f"Duplicate {item['first_name']} {item['surname']}. skip or overwrite? ").strip().lower()
                    if answer == "overwrite":
                        overwrite = True
                    else:
                        print("Skipped.")
                        continue

                insert_contact_from_dict(cur, item, overwrite)

        conn.commit()
        print("CSV import completed.")
    except Exception as e:
        conn.rollback()
        print("Error while importing CSV:", e)
    finally:
        cur.close()
        conn.close()


def menu():
    while True:
        print("\n--- TSIS1 PHONEBOOK MENU ---")
        print("1. Add contact")
        print("2. Show all contacts")
        print("3. Filter by group")
        print("4. Search by email")
        print("5. Search all fields")
        print("6. Sort contacts")
        print("7. Paginated navigation")
        print("8. Export to JSON")
        print("9. Import from JSON")
        print("10. Import from CSV")
        print("11. Add phone using procedure")
        print("12. Move contact to group using procedure")
        print("13. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            add_contact_interactive()
        elif choice == "2":
            show_all_contacts()
        elif choice == "3":
            filter_by_group()
        elif choice == "4":
            search_by_email()
        elif choice == "5":
            search_all_fields()
        elif choice == "6":
            sort_contacts_menu()
        elif choice == "7":
            paginated_navigation()
        elif choice == "8":
            export_to_json()
        elif choice == "9":
            import_from_json()
        elif choice == "10":
            import_from_csv()
        elif choice == "11":
            add_phone_procedure()
        elif choice == "12":
            move_to_group_procedure()
        elif choice == "13":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()
