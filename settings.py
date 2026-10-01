import os

# Шлях до папки проєкту
PATH = os.path.dirname(__file__) + os.sep

# Шлях до бази даних
DB_NAME = 'blog.db'
PATH_DB = PATH + DB_NAME

PATH_STATIC = PATH + 'static' + os.sep
PATH_UPLOADS = PATH_STATIC + 'uploads' + os.sep

# Секретний ключ
SECRET_KEY = 'X9#mK2@pL7!qR4$nT8&wY1^vZ3*'