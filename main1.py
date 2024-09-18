import streamlit as st
import hashlib
import sqlite3
from datetime import datetime

# Constantes para mensagens
WELCOME_MSG = "****************************************\n*** Caixa Eletrônico ***\n****************************************"
INSTRUCTIONS_MSG = """
Bem-vindo ao Caixa Eletrônico da School of Net!
Por favor, siga as instruções abaixo para acessar sua conta:

1. Digite o número da sua conta quando solicitado.
2. Digite sua senha quando solicitado.
3. Após o login, você poderá realizar operações bancárias.

Se você encontrar qualquer problema, por favor, entre em contato com o suporte.
"""

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(account, password):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM accounts WHERE account = ?', (account,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True
    return False

def get_account_info(account):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, value FROM accounts WHERE account = ?', (account,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_balance(account, amount):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE accounts SET value = value + ? WHERE account = ?', (amount, account))
    conn.commit()
    conn.close()

def add_transaction(account, type, amount):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO transactions (account, type, amount, timestamp) VALUES (?, ?, ?, ?)', (account, type, amount, timestamp))
    conn.commit()
    conn.close()

def get_transactions(account):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('SELECT type, amount, timestamp FROM transactions WHERE account = ? ORDER BY id', (account,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def show_balance(account):
    name, balance = get_account_info(account)
    st.subheader("Saldo")
    st.info(f"Seu saldo é: R$ {balance:.2f}")
    st.subheader("Histórico de Transações")
    transactions = get_transactions(account)
    for i, transaction in enumerate(transactions, start=1):
        st.write(f"{i}. {transaction[2]} - {transaction[0]} de R$ {transaction[1]:.2f}")

def withdraw(account):
    name, balance = get_account_info(account)
    st.subheader("Saque")
    st.info(f"Seu saldo é: R$ {balance:.2f}")
    amount = st.number_input('Digite o valor para saque:', min_value=0.0, step=10.0, key='withdraw_amount')
    if st.button('Confirmar Saque', key='confirm_withdraw'):
        if amount <= balance:
            update_balance(account, -amount)
            add_transaction(account, 'Saque', amount)
            st.success(f"Saque de R$ {amount:.2f} realizado com sucesso!")
            show_balance(account)
        else:
            st.error("Saldo insuficiente para realizar o saque.")

def deposit(account):
    name, balance = get_account_info(account)
    st.subheader("Depósito")
    st.info(f"Seu saldo é: R$ {balance:.2f}")
    amount = st.number_input('Digite o valor para depósito:', min_value=0.0, step=10.0, key='deposit_amount')
    if st.button('Confirmar Depósito', key='confirm_deposit'):
        update_balance(account, amount)
        add_transaction(account, 'Depósito', amount)
        st.success(f"Depósito de R$ {amount:.2f} realizado com sucesso!")
        show_balance(account)

def logout():
    st.info("Você saiu da sua conta.")
    st.session_state.logged_in = False
    st.session_state.account = None
    st.experimental_rerun()

def show_account_options(account):
    st.sidebar.subheader("Operações Disponíveis")
    option = st.sidebar.selectbox("Escolha uma operação", ["Verificar Saldo", "Saque", "Depósito", "Logout"])
    
    name, _ = get_account_info(account)
    st.subheader(f"Bem-vindo, {name}!")
    st.write(f"Conta: {account}")
    
    if option == "Verificar Saldo":
        show_balance(account)
    elif option == "Saque":
        withdraw(account)
    elif option == "Depósito":
        deposit(account)
    elif option == "Logout":
        logout()

def main():
    st.title("Caixa Eletrônico - School of Net")
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.account = None

    if not st.session_state.logged_in:
        st.write(WELCOME_MSG)
        st.write(INSTRUCTIONS_MSG)
        
        account_typed = st.text_input('Digite sua conta:')
        password_typed = st.text_input('Digite sua senha:', type="password")
        
        if st.button('Login'):
            if authenticate(account_typed, password_typed):
                st.session_state.logged_in = True
                st.session_state.account = account_typed
                st.success(f"Bem-vindo, {get_account_info(account_typed)[0]}!")
            else:
                st.error("Conta ou senha inválida. Tente novamente.")
    else:
        show_account_options(st.session_state.account)

if __name__ == "__main__":
    main()
    
# fim