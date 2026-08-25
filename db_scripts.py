import sqlite3
from settings import *


conn = None
cursor = None


# Відкрити з'єднання з базою даних
def open_db():
    global conn, cursor
    conn = sqlite3.connect(PATH_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')


# Закрити з'єднання з базою даних
def close_db():
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# Виконати SQL-запит
def execute(query, params=None):
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)
    conn.commit()


# Створити таблиці в базі даних
def create_tables():
    open_db()

    execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL
        )
    ''')

    execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            image TEXT,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            description_short TEXT,
            description TEXT
        )
    ''')

    execute('''
        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
    ''')

    close_db()


# Отримати одного користувача
def get_user():
    open_db()
    cursor.execute('SELECT * FROM users')
    user = cursor.fetchone()
    close_db()

    return user


# Отримати всі категорії
def get_categories():
    open_db()
    cursor.execute('SELECT * FROM categories ORDER BY category_id')
    categories = cursor.fetchall()
    close_db()

    return categories


# Додати нову категорію
def add_category(category_name):
    open_db()
    execute('INSERT INTO categories (category_name) VALUES (?)', [category_name])
    close_db()


# Отримати один пост
def get_post(post_id):
    open_db()
    cursor.execute(
        '''
        SELECT * FROM posts
        WHERE post_id = ?
        ''',
        [post_id]
    )
    post = cursor.fetchone()
    close_db()

    return post


# Отримати всі пости певної категорії
def get_posts(category_id):
    open_db()
    cursor.execute('''
        SELECT * FROM posts, categories
        WHERE posts.category_id = categories.category_id
        AND posts.category_id = ?
        ORDER BY posts.datetime DESC
    ''', [category_id])
    posts = cursor.fetchall()
    close_db()

    return posts


# отримати категорію по id
def get_category(category_id):
    open_db()
    cursor.execute(
        '''SELECT * FROM categories WHERE category_id = ?''',
        [category_id]
    )
    category = cursor.fetchone()
    close_db()

    return category

# отримати категорію по її назві
def get_category_by_name(category_name):
    open_db()
    cursor.execute(
        '''SELECT * FROM categories WHERE category_name = ?''',
        [category_name]
    )
    category = cursor.fetchone()
    close_db()

    return category


# Додати новий пост
def add_post(category_id, text, title, image, datetime=None):
    open_db()

    if datetime is None:
        execute('''
            INSERT INTO posts (category_id, text, title, image)
            VALUES (?, ?, ?, ?)
        ''', [category_id, text, title, image])
    else:
        execute('''
            INSERT INTO posts (category_id, text, title, image, datetime)
            VALUES (?, ?, ?, ?, ?)
        ''', [category_id, text, title, image, datetime])

    close_db()

# Отримати всі дані користувача
def get_user():
    open_db()
    cursor.execute('''SELECT * FROM users''')
    user = cursor.fetchone()
    close_db()
    
    return user

# Очистити таблиці для тестування
def clear_tables():
    open_db()
    execute('DELETE FROM posts')
    execute('DELETE FROM categories')
    execute("DELETE FROM sqlite_sequence WHERE name = 'posts'")
    execute("DELETE FROM sqlite_sequence WHERE name = 'categories'")
    close_db()


# Вивести пости у зручному вигляді
def show_posts(category_id):
    posts = get_posts(category_id)

    for post in posts:
        print('Текст:', post['text'])
        print('Категорія:', post['category_name'])
        print('Дата публікації:', post['datetime'])
        print('-' * 50)


def del_post(post_id):
    open_db()
    cursor.execute('''DELETE FROM posts WHERE post_id=(?)''', [post_id])
    conn.commit()
    close_db()


if __name__ == "__main__":
    create_tables()
    clear_tables()

    # Додаємо категорії
    add_category('gamedev')
    add_category('web')
    add_category('personal')

    # Додаємо пости
    add_post(
        1,
        'На цьому модулі я створив свою першу просту мобільну гру та навчився працювати з основними елементами гри.', 
        '2026-03-14 18:40' # Можна вказати дату явно або вона буде встановлена за замовчуванням як в наступних випадках
    )

    add_post(
        1,
        'На цьому модулі я познайомився з основами створення 3D гри у Godot, навчився працювати з об’єктами сцени та зрозумів, як будуються тривимірні світи.'
    )

    add_post(
        2,
        'Я дізнався, як працюють HTML і CSS, та зрозумів, як створюються прості веб-сторінки.'
    )

    add_post(
        3,
        'Я розповів про гру, яка надихнула мене, і пояснив, чому саме вона мені найбільше подобається.'
    )

    print('Пости категорії GameDev')
    print('=' * 50)
    show_posts(1)

    print('\nПости категорії Web')
    print('=' * 50)
    show_posts(2)

    print('\nПости категорії Особисте')
    print('=' * 50)
    show_posts(3)