import sqlite3

def setup_database():
    conn = sqlite3.connect(":memory:")  # Используем in-memory базу данных для теста
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, name TEXT, score INTEGER)''')
    conn.commit()
    return conn, cursor

def user_exists(cursor, name):
    cursor.execute("SELECT 1 FROM scores WHERE name = ?", (name,))
    return cursor.fetchone() is not None

def save_score(cursor, conn, name, score):
    if not name.strip():  # Проверяем, что имя не пустое
        return False
    if not user_exists(cursor, name):
        cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
        conn.commit()
        return True
    return False

def test_existing_user_registration():
    conn, cursor = setup_database()
    name = "Player1"
    score = 100
    
    # Первая регистрация должна сработать
    assert save_score(cursor, conn, name, score) == True
    
    # Повторная регистрация не должна сработать
    assert save_score(cursor, conn, name, 200) == False
    
    conn.close()
    print("Тест пройден: регистрация уже существующего пользователя не срабатывает.")

def test_empty_name_registration():
    conn, cursor = setup_database()
    empty_name = ""
    score = 100
    
    # Регистрация с пустым именем не должна срабатывать
    assert save_score(cursor, conn, empty_name, score) == False
    
    conn.close()
    print("Тест пройден: метод AddUser не вызывается, если имя пустое.")

# Запуск тестов
test_existing_user_registration()
test_empty_name_registration()
