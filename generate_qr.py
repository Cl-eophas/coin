import qrcode
import sqlite3
from PIL import Image

def create_database():
    conn = sqlite3.connect('user_database.db')
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        conn.commit()
    finally:
        conn.close()

def add_user(name, email, phone):
    conn = sqlite3.connect('user_database.db')
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, phone)
            VALUES (?, ?, ?)
        ''', (name, email, phone))
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        print("Error: Email must be unique.")
        return None
    finally:
        conn.close()

def view_users():
    conn = sqlite3.connect('user_database.db')
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, phone FROM users")
        users = cursor.fetchall()
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Phone: {user[3]}")
    finally:
        conn.close()

def generate_qr_from_database(user_id):
    conn = sqlite3.connect('user_database.db')
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user_data = cursor.fetchone()
        if not user_data:
            print("User not found.")
            return

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(user_data))
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(f'user_{user_id}_qr.png')
        print(f"QR code saved as user_{user_id}_qr.png")
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()

    while True:
        action = input("Choose action: 'add' to add user, 'view' to view users, 'exit' to quit: ")
        if action.lower() == 'exit':
            break
        elif action.lower() == 'add':
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            phone = input("Enter user phone: ")
            user_id = add_user(name, email, phone)
            if user_id:
                generate_qr_from_database(user_id)
                print("QR code generated successfully.")
        elif action.lower() == 'view':
            view_users()