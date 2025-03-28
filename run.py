import sqlite3

from flask import Flask, render_template, redirect, request, flash, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/visit_geeksforgeeks')
def visit_geeksforgeeks():
    return redirect('https://www.geeksforgeeks.org')
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        # Получаем данные из формы
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        role = request.form.get('role')

        # Проверяем, что все поля заполнены
        if not first_name or not last_name or not password or not role:
            flash('Все поля обязательны для заполнения', 'error')
            return redirect(url_for('admin_panel'))

        # Проверяем, что пользователь с таким логином не существует
        con = sqlite3.connect('db/orders.db')


        cursor = con.cursor()
        result = cursor.execute("""SELECT * FROM users
                            WHERE userid = userid""").fetchall()

    if existing_user:
            flash('Пользователь с таким именем и фамилией уже существует', 'error')
            return redirect(url_for('admin_panel'))

        # Создаем нового пользователя
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            password_hash=generate_password_hash(password),  # Хэшируем пароль
            role=role
        )

        # Сохраняем пользователя в базу данных
        db.session.add(new_user)
        db.session.commit()

        flash('Пользователь успешно добавлен', 'success')
        return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)
