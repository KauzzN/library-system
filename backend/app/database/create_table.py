from app.database.connection import connection, cursor

query = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        name TEXT NOT NULL,
        
        email TEXT UNIQUE NOT NULL,
        
        password TEXT NOT NULL
    );
"""

cursor.execute(query)

connection.commit()

print("Tabela users criada")
