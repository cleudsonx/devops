import sqlite3
import hashlib

def create_database():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    
    # Criar tabela de contas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        value REAL NOT NULL,
        admin BOOLEAN NOT NULL
    )
    ''')
    
    # Criar tabela de transações
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account TEXT NOT NULL,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (account) REFERENCES accounts (account)
    )
    ''')
    
    # Inserir dados iniciais
    cursor.execute('''
    INSERT OR IGNORE INTO accounts (account, password, name, value, admin) VALUES
    ('0001-02', ?, 'Fulano da Silva', 100, 0),
    ('0002-02', ?, 'Cicrano da Silva', 50, 0),
    ('1111-11', ?, 'Admin da Silva', 1000, 1)
    ''', (hashlib.sha256('123456'.encode()).hexdigest(), hashlib.sha256('123456'.encode()).hexdigest(), hashlib.sha256('123456'.encode()).hexdigest()))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()