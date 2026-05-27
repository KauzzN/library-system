from app.database.connection import connection, cursor

query = """        
        
        CREATE TABLE IF NOT EXISTS loans( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT NOT NULL, book_id INT NOT NULL, customer_name VARCHAR(120) NOT NULL, customer_phone VARCHAR(20), status VARCHAR(20) DEFAULT 'borrowed', loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, return_date TIMESTAMP NULL, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(book_id) REFERENCES books(id) );
"""

cursor.execute(query)

connection.commit()

print("Tabela users criada")
