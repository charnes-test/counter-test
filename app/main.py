import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)

# Данные для подключения
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('POSTGRES_DB', 'counter_db')
DB_USER = os.environ.get('POSTGRES_USER', 'user')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'password')


def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            print("Waiting for DB...")
            time.sleep(2)
    return None


@app.route('/')
def hello():
    conn = get_db_connection()
    if not conn:
        return "Error connecting to Database", 500

    cur = conn.cursor()
    # увеличиваем счетчик
    cur.execute('UPDATE visits SET count = count + 1 WHERE id = 1 RETURNING count;')
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return f'Эту страницу посетили {count} раз.\n'


# сброс
@app.route('/reset')
def reset():
    conn = get_db_connection()
    if not conn:
        return "Error connecting to Database", 500

    cur = conn.cursor()
    # в 0
    cur.execute('UPDATE visits SET count = 0 WHERE id = 1;')
    conn.commit()
    cur.close()
    conn.close()
    return 'Счетчик успешно сброшен.\n'



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)