import pymysql
import requests

import time


# Подключение к базе данных MySQL
def get_db_connection():
    return pymysql.connect(
        host="localhost",  # Замените на ваш хост
        user="atatek",  # Замените на вашего пользователя
        password="atatek",  # Замените на ваш пароль
        database="atatek",  # Замените на вашу базу данных
        cursorclass=pymysql.cursors.DictCursor  # Для работы с результатами как с словарями
    )


# Функция для получения данных из API
def get_tree_data_on_request(id):
    url = f'https://tumalas.kz/wp-admin/admin-ajax.php?action=tuma_cached_childnew_get&nodeid=14&id={id}'
    response = requests.get(url)
    return response.json()


# Функция для сохранения данных в базу данных
def create_tree(cursor, name, item_id, parent_id, birth, death, created_by):
    try:
        query = """
            INSERT INTO main_tree (name, item_id, parent_id, birth, death, created_by, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, item_id, parent_id, birth, death, created_by, False))  # status = False
    except pymysql.MySQLError as err:
        print(f"Ошибка при добавлении данных: {err}")


# Функция для обработки данных с API и их сохранения в базе
def get_data_and_save(id, cursor):
    data = get_tree_data_on_request(id)
    for item in data:
        # Проверка на существование записи в базе
        query = "SELECT * FROM main_tree WHERE item_id = %s"
        cursor.execute(query, (item['id'],))
        existing_item = cursor.fetchone()

        if not existing_item:
            create_tree(cursor, item['name'], item['id'], id, item['birth_year'], item['death_year'], created_by=1)


# Основная функция для поиска и обработки элементов с status = 0
def find_and_process_tree():
    connection = get_db_connection()
    cursor = connection.cursor()

    while True:
        # Находим первый элемент с status == 0
        query = "SELECT * FROM main_tree WHERE status = 0 LIMIT 1"
        cursor.execute(query)
        tree_item = cursor.fetchone()

        if tree_item:
            item_id = tree_item['item_id']
            print(f"Обрабатываем элемент с item_id = {item_id}")
            get_data_and_save(item_id, cursor)
            connection.commit()  # Сохраняем изменения в базе
            print("Обработка завершена, элемент найден.")
            break  # Прерываем цикл, если элемент найден
        else:
            print("Элемент с status = 0 не найден, ждем 5 секунд...")
            time.sleep(5)  # Ждем 5 секунд перед повторным запросом

    cursor.close()
    connection.close()


# Основная функция для выполнения до тех пор, пока не будет найден элемент с status = 0
if __name__ == "__main__":
    print("Запуск процесса обработки данных...")
    find_and_process_tree()
    print("Процесс завершен.")
