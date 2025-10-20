import sqlite3
from sqlite3 import Error
import os
from unicodedata import name


DB_FILE = "arte_no_copo.db"

def criar_conexao(db_file):
    """Cria uma conexão com o banco de dados SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conexão estabelecida com SQLite: {db_file}")
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def executar_sql(conn, sql):
    """Executa um comando SQL (DDL ou DML)."""
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Error as e:
        print(f"Erro ao executar SQL: {e}")

def criar_tabelas(conn):
    """Cria todas as tabelas do esquema 'Arte no Copo DB'."""
    print("Criando tabelas...")
    
   
    sql_cliente = """
    CREATE TABLE IF NOT EXISTS Cliente (
        cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        email TEXT UNIQUE NOT NULL
    );"""
    
   
    sql_produto = """
    CREATE TABLE IF NOT EXISTS Produto (
        produto_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_produto TEXT UNIQUE NOT NULL,
        descricao TEXT,
        preco REAL NOT NULL, -- SQLite usa REAL para valores decimais
        categoria TEXT NOT NULL,
        tema_gatinho TEXT
    );"""
    
  
    sql_arte = """
    CREATE TABLE IF NOT EXISTS ArteNoCopo (
        arte_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_arte TEXT UNIQUE NOT NULL,
        custo_adicional REAL DEFAULT 0.00,
        disponivel INTEGER DEFAULT 1 -- 1 para TRUE, 0 para FALSE
    );"""

   
    sql_pedido = """
    CREATE TABLE IF NOT EXISTS Pedido (
        pedido_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        data_hora_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        valor_total REAL NOT NULL,
        status_pedido TEXT NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id)
    );"""

   
    sql_item_pedido = """
    CREATE TABLE IF NOT EXISTS ItemPedido (
        item_pedido_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        arte_id INTEGER,
        quantidade INTEGER NOT NULL,
        preco_unitario REAL NOT NULL,
        observacoes TEXT,
        FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id),
        FOREIGN KEY (produto_id) REFERENCES Produto(produto_id),
        FOREIGN KEY (arte_id) REFERENCES ArteNoCopo(arte_id)
    );"""

    executar_sql(conn, sql_cliente)
    executar_sql(conn, sql_produto)
    executar_sql(conn, sql_arte)
    executar_sql(conn, sql_pedido)
    executar_sql(conn, sql_item_pedido)
    print("Tabelas criadas com sucesso.")

def inserir_dados_exemplo(conn):
    """Insere dados fictícios nas tabelas."""
    print("Inserindo dados de exemplo...")
    cursor = conn.cursor()

    
    clientes = [
        ("Maria de Souza", "11988887777", "maria@gatoscafe.com"),
        ("João Silva", "21966665555", "joao@gatoscafe.com")
    ]
    cursor.executemany("INSERT INTO Cliente (nome, telefone, email) VALUES (?, ?, ?)", clientes)

   
    produtos = [
        ("Latte Ronronado", "Café cremoso com leite de aveia.", 15.50, "Café", "Pata de Gato"),
        ("Chá Felino da Tarde", "Chá de frutas vermelhas e especiarias.", 12.00, "Chá", "Bigodes"),
        ("Pão de Queijo Aconchego", "Pão de queijo quentinho e crocante.", 6.00, "Salgado", None)
    ]
    cursor.executemany("INSERT INTO Produto (nome_produto, descricao, preco, categoria, tema_gatinho) VALUES (?, ?, ?, ?, ?)", produtos)
    
    
    artes = [
        ("Latte Art - Gatinho Dormindo", 3.00, 1),
        ("Copo Personalizado - Fundo Bege", 5.00, 1),
        ("Borda de Chocolate - Pata", 2.50, 1)
    ]
    cursor.executemany("INSERT INTO ArteNoCopo (nome_arte, custo_adicional, disponivel) VALUES (?, ?, ?)", artes)

    conn.commit()
    print("Dados de exemplo inseridos com sucesso.")


def main():
    
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = criar_conexao(DB_FILE)
    
    if conn is not None:
        criar_tabelas(conn)
        inserir_dados_exemplo(conn)
        
       
        print("\n--- Clientes Cadastrados ---")
        cursor = conn.cursor()
        for row in cursor.execute("SELECT * FROM Cliente;"):
            print(row)
            
        conn.close()
    else:
        print("Não foi possível continuar sem uma conexão com o banco de dados.")

if  name == '_main_':
 main()