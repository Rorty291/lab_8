import psycopg2
import os

# --- STUDENT TODO: ---

DB_NAME = "online_shop"
DB_USER = "postgres"
DB_PASS = os.getenv("DB_PASSWORD", "rorty_pass")
DB_HOST = "localhost"
DB_PORT = "5432"


def print_commands():
    print("-------------------")
    print("1. Insert")
    print("2. Update")
    print("3. Delete")
    print("4. Select")
    print("0. Exit")
    print("-------------------\n")

def main():
    conn = None  # Initialize conn to None
    try:
        # Establish the connection
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Database connected successfully")
        cur = conn.cursor()

        # --- STUDENT TODO: Task 3 - Create Table ---

        create_table_query = """
             CREATE TABLE IF NOT EXISTS orders (
             id SERIAL PRIMARY KEY,
             client VARCHAR(100) NOT NULL,
             order_number INTEGER,
             order_date DATE,
             sum_price INTEGER NOT NULL
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        print("Table 'orders' created successfully.")

        while True:
            try:
                print_commands()
                command = input("Введіть команду")
                if command == "0":
                    break
                elif command == "1":
                    order_data = []
                    while True:
                        try:
                            if len(order_data) != 0:
                                choice = input("Додати ще? y/n")
                                if choice == "n":
                                    break

                            name = input("Введіть ім'я.")
                            order = int(input("Введіть номер замовлення."))
                            date = input("Введіть дату. (ex. 2026-11-26)")
                            sum_price = int(input("Введіть суму замовлення."))

                            order_data.append((name, order, date, sum_price))
                        except ValueError:
                            continue
                        except KeyboardInterrupt:
                            break

                    print(order_data)
                    insert_query = "INSERT INTO orders (client, order_number, order_date, sum_price) VALUES (%s, %s, %s, %s)"
                    cur.executemany(insert_query, order_data)
                    conn.commit()
                    print(f"{cur.rowcount} records inserted successfully.")
                elif command == "2":
                    change_param = input("Введіть який параметр змінити. (client/order_number/order_date/sum_price)")
                    if not change_param in ("client", "order_number", "order_date", "sum_price"):
                        raise ValueError("Невірна назва параметру.")

                    change_value = input("Введіть нове значення параметру.")
                    if change_param in ("client", "order_date"):
                        change_value = f"'{change_value}'"
                    else:
                        change_value = int(change_value)

                    search_param = input("Введіть який параметр шукати. (client/order_number/order_date/sum_price)")
                    if not search_param in ("client", "order_number", "order_date", "sum_price"):
                        raise ValueError("Невірна назва параметру.")

                    search_value = input("Введіть значення шуканого параметру.")
                    if search_param in ("client", "order_date"):
                        search_value = f"'{search_value}'"
                    else:
                        search_value = int(search_value)

                    if search_value == change_value and change_param == search_param:
                        raise ValueError("Значення обох параметрів однакові")

                    update_query = f"UPDATE orders SET {change_param} = {change_value} WHERE {search_param} = {search_value};"
                    cur.execute(update_query)
                    conn.commit()
                    print(f"{cur.rowcount} record(s) updated successfully.")
                elif command == "3":
                    search_param = input("Введіть який параметр шукати. (client/order_number/order_date/sum_price)")
                    if not search_param in ("client", "order_number", "order_date", "sum_price"):
                        raise ValueError("Невірна назва параметру.")

                    search_value = input("Введіть значення шуканого параметру.")
                    if search_param in ("client", "order_date"):
                        search_value = f"'{search_value}'"
                    else:
                        search_value = int(search_value)

                    delete_query = f"DELETE FROM orders WHERE {search_param} = {search_value};"
                    cur.execute(delete_query)
                    conn.commit()
                    print(f"{cur.rowcount} record(s) deleted successfully.")
                elif command == "4":
                    search_param = input("Введіть який параметр шукати. (client/order_number/order_date/sum_price)")
                    if not search_param in ("client", "order_number", "order_date", "sum_price"):
                        raise ValueError("Невірна назва параметру.")

                    order_param = input("Введіть вид сортування. ASC/DESC")
                    if not order_param in ("ASC", "DESC"):
                        raise ValueError("Невірний тип сортування.")

                    select_query = f"SELECT * FROM orders ORDER BY {search_param} {order_param};"
                    cur.execute(select_query)
                    records = cur.fetchall()
                    print("\n--- Order Records ---")
                    for record in records:
                        print(
                            f"Client: {record[1]}, Order ID: {record[2]}, Order Date: {record[3]}, Order Price: {record[4]}")
                    print("-----------------------\n")
            except ValueError as error:
                print(error)
                continue
            except KeyboardInterrupt as error:
                print(error)
                break

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while connecting to PostgreSQL: {error}")

    finally:
        # Ensure the connection is closed
        if conn is not None:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()