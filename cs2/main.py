import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session

smoke_halper_cs = Flask(__name__)
DATABASE = 'database.db'

@smoke_halper_cs.route('/', methods=['GET', 'POST'])
def login():
    site_name = "SH - Авторизация"

    user_login = None
    user_password = None

    login_error = None
    pas_error = None

    if request.method == 'POST':
        user_login = request.form.get('name')
        user_password = request.form.get('password')
        if not user_login or not user_password:
            login_error = "Поля не могут быть пустыми"
        else:

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('SELECT password from users where name = ?', (user_login,))
            result = cursor.fetchone()
            conn.close()

            if result is None:
                login_error = "Логин не зарегистрирован"
            else:
                db_password = result[0]
                if db_password == user_password:

                    return redirect(url_for("main"))
                else:
                    pas_error = "Неверный пароль"

    return render_template("login.html", titel = site_name, name = user_login,password = user_password, error = login_error, pas = pas_error)

@smoke_halper_cs.route('/register', methods=['GET', 'POST'])
def register():
    site_name = "SH - Регистрация"
    register_error = None
    success = None

    if request.method == 'POST':
        user_login = request.form.get('name')
        user_password = request.form.get('password')

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (user_login, user_password))
            conn.commit()
            conn.close()
            success = "YPA"
        except sqlite3.IntegrityError:
            register_error = "Имя занято"

    return render_template("register.html", titel=site_name, success=success, register_error=register_error)

@smoke_halper_cs.route('/main', methods=['GET', 'POST'])
def main():

    return render_template("main.html")

@smoke_halper_cs.route('/dust2', methods=['GET', 'POST'])
def dust2():
    site_name = "SmokeHalper - Dust2"

    return render_template("dust2.html", titel=site_name)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        password TEXT NOT NULL)
    """)

if __name__ == '__main__':
    init_db()
    smoke_halper_cs.run(debug=True)

