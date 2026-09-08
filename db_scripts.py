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
            title TEXT,
            image TEXT,
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

def update_first_user(name, image, description_short, description ):
    open_db()
    cursor.execute('SELECT user_id FROM users ORDER BY user_id LIMIT 1')
    user = cursor.fetchone()

    if user:
        execute('''
            UPDATE users
            SET name = ?, image = ?, description_short = ?, description = ?
            WHERE user_id = ?
        ''', [name, image, description_short, description, user['user_id']])
    else:
        execute('''
            INSERT INTO users (name, image, login, password, description_short, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [name, image, 'student', 'student', description_short, description])
    close_db()

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

    update_first_user(
        'Тетяна',
        'my_photo.png',
        'Мене звати Таня, мені 27 років, і я викладач програмування. Навчаю мислити як розробник, а не просто писати код. Вірю, що IT — це творчість, тому на заняттях поєдную логіку з грою. Поза роботою читаю книжки (від класики до нон-фікшн) і займаюся спортом, бо для крутого коду потрібен енергійний мозок і здорове тіло.',
        'Мене звати Таня, мені 27 років, і я викладач програмування в школі для дітей та підлітків. Моя головна задача — не просто навчити синтаксису Python або JavaScript, а прищепити любов до алгоритмів, навчити розбивати складні задачі на прості кроки та не боятися помилок (бо помилка — це перший крок до нового знання).Я обожнюю спостерігати, як в очах учнів спалахує вогник, коли їхній код працює вперше. Намагаюся створювати на заняттях атмосферу дослідження, а не сухої теорії. У вільний час я завжди з книжкою — читаю художню літературу для натхнення та професійну літературу, щоб бути в тренді. А ще спорт допомагає мені тримати баланс: після годин за комп''ютером я йду на тренування, щоб перезавантажити голову та зарядитися енергією для нових уроків. Переконана, що найкращі програмісти — це ті, хто вміє навчатися все життя, і я показую це власним прикладом.'
        )

    # Додаємо категорії
    add_category('gamedev')
    add_category('web')
    add_category('personal')

    # Додаємо пости
    add_post(
        1,
        'На цьому модулі я створив свою першу просту мобільну гру та навчився працювати з основними елементами гри.',
        'Моя перша мобільна гра',
        None,
        '2026-03-14 18:40' # Можна вказати дату явно або вона буде встановлена за замовчуванням як в наступних випадках
    )

    add_post(
        1,
        'На цьому модулі я познайомився з основами створення 3D гри у Godot, навчився працювати з об’єктами сцени та зрозумів, як будуються тривимірні світи.',
        'Перші кроки у 3D грі',
        None
    )

    add_post(
        2,
        'Я дізнався, як працюють HTML і CSS, та зрозумів, як створюються прості веб-сторінки.',
        'Знайомство з HTML і CSS',
        None
    )

    add_post(
        3,
        'Я розповів про гру, яка надихнула мене, і пояснив, чому саме вона мені найбільше подобається.',
        'Гра, яка мене надихнула',
        None
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