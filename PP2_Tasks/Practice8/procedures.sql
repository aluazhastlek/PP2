-- 1) Procedure: upsert one contact
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE first_name = p_first_name
          AND surname = p_surname
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE first_name = p_first_name
          AND surname = p_surname;
    ELSE
        INSERT INTO phonebook(first_name, surname, phone)
        VALUES (p_first_name, p_surname, p_phone);
    END IF;
END;
$$;


-- 2) Procedure: delete by username or phone
CREATE OR REPLACE PROCEDURE delete_contact_proc(
    p_first_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_first_name IS NOT NULL THEN
        DELETE FROM phonebook
        WHERE first_name = p_first_name;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM phonebook
        WHERE phone = p_phone;
    ELSE
        RAISE EXCEPTION 'Provide either first_name or phone';
    END IF;
END;
$$;


-- 3) Bulk insert with validation
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_first_names TEXT[],
    p_surnames TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    arr_len INT;
BEGIN
    arr_len := array_length(p_first_names, 1);

    IF arr_len IS NULL
       OR arr_len <> array_length(p_surnames, 1)
       OR arr_len <> array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'All arrays must have the same length and not be empty';
    END IF;

    FOR i IN 1..arr_len LOOP
        IF p_phones[i] ~ '^[0-9]{11}$' THEN
            IF EXISTS (
                SELECT 1
                FROM phonebook
                WHERE first_name = p_first_names[i]
                  AND surname = p_surnames[i]
            ) THEN
                UPDATE phonebook
                SET phone = p_phones[i]
                WHERE first_name = p_first_names[i]
                  AND surname = p_surnames[i];
            ELSE
                INSERT INTO phonebook(first_name, surname, phone)
                VALUES (p_first_names[i], p_surnames[i], p_phones[i]);
            END IF;
        ELSE
            RAISE NOTICE 'Incorrect data: %, %, %',
                p_first_names[i], p_surnames[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;
