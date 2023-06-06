import mysql.connector

config = {
    'user':  'root',
    'password': 'REDACTED',
    'host': 'localhost',
    'database': 'paragraphs'
}

def get_random_paragraph():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT paragraph FROM paragraph_storage ORDER BY RAND() LIMIT 1')
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0]

