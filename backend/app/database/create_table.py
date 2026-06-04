from app.database.connection import connection, cursor

query = """        
    CREATE TABLE IF NOT EXISTS password_resets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        token TEXT NOT NULL,

        expires_at TIMESTAMP NOT NULL,

        used INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
);
"""

cursor.execute(query)

connection.commit()

print("Tabela users criada")
