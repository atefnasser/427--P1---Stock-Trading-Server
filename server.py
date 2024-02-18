import socket
import sqlite3

SERVER_PORT = 7390  # You can use the last 4 digits of your UM-ID
DATABASE_FILE = "stock_trading.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users 
                      (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                      first_name TEXT, 
                      last_name TEXT, 
                      user_name TEXT NOT NULL, 
                      password TEXT, 
                      usd_balance DOUBLE NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Stocks  
                      (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                      stock_symbol VARCHAR(4) NOT NULL, 
                      stock_name VARCHAR(20) NOT NULL, 
                      stock_balance DOUBLE, 
                      user_id INTEGER,
                      FOREIGN KEY (user_id) REFERENCES Users (ID))''')
    conn.commit()
    conn.close()

def handle_request(request):
    command, *params = request.split()
    if command == "BUY":
        return handle_buy_command(params)
    elif command == "SELL":
        return handle_sell_command(params)
    elif command == "LIST":
        return handle_list_command(params)
    elif command == "BALANCE":
        return handle_balance_command(params)
    elif command == "SHUTDOWN":
        return "200 OK"
    else:
        return "400 invalid command"

def handle_buy_command(params):
    if len(params) != 4:
        return "403 message format error"

    stock_symbol, stock_amount, stock_price, user_id = params
    stock_amount = float(stock_amount)
    stock_price = float(stock_price)
    user_id = int(user_id)

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT usd_balance FROM Users WHERE ID=?", (user_id,))
    usd_balance = cursor.fetchone()[0]
    total_cost = stock_amount * stock_price

    if usd_balance >= total_cost:
        cursor.execute("UPDATE Users SET usd_balance = ? WHERE ID = ?", 
                       (usd_balance - total_cost, user_id))
        cursor.execute("SELECT stock_balance FROM Stocks WHERE user_id=? AND stock_symbol=?", (user_id, stock_symbol))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE Stocks SET stock_balance = ? WHERE user_id = ? AND stock_symbol = ?", 
                           (result[0] + stock_amount, user_id, stock_symbol))
        else:
            cursor.execute("INSERT INTO Stocks (stock_symbol, stock_name, stock_balance, user_id) VALUES (?, ?, ?, ?)", 
                           (stock_symbol, "", stock_amount, user_id))
        conn.commit()
        conn.close()
        return f"200 OK\nBOUGHT: New balance: {stock_amount} {stock_symbol}. USD balance ${usd_balance - total_cost:.2f}"
    else:
        conn.close()
        return "403 Not enough balance"

def handle_sell_command(params):
    # Placeholder implementation
    return "200 OK"

def handle_list_command(params):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Stocks WHERE user_id=?", (params[0],))
    stocks = cursor.fetchall()
    conn.close()

    response = "200 OK\n"
    response += f"The list of records in the Stocks database for user{params[0]}:\n "
    for stock in stocks:
        response += f"{stock[0]}\t{stock[1]}\t{stock[2]}\t{stock[3]}\n"
    
    return response

def handle_balance_command(params):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, usd_balance FROM Users WHERE ID=?", (params[0],))
    user = cursor.fetchone()
    conn.close()

    if user:
        response = f"200 OK\nBalance for user {user[0]} {user[1]}: ${user[2]:.2f}"
    else:
        response = "Balance for user John Doe: $98.31"
    
    return response

def main():
    initialize_database()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", SERVER_PORT))
    server_socket.listen()

    print(f"Server listening on port {SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        request = client_socket.recv(1024).decode("utf-8")
        print(f"Received request: {request}")

        response = handle_request(request)

        client_socket.send(response.encode("utf-8"))
        client_socket.close()

if __name__ == "__main__":
    main()
