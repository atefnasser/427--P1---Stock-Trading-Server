# Stock Trading Server

This is a simple stock trading server implemented in Python using sockets. It allows clients to connect and perform various operations such as buying, selling, listing stocks, checking balances, and shutting down the server.

## Usage

1. Run the `server.py` script to start the server.
2. Run the `client.py` script to interact with the server.
3. Follow the prompts in the client to perform operations on the stock market.
4. Use the `QUIT` command to exit the client.


## Bugs in the Code
- SELL command not fully implemented; placeholder exists but lacks functionality.
- Error handling for invalid user input is minimal, which might cause unexpected crashes.
- Database transactions are not atomic, potentially leading to data inconsistencies under concurrent access.

## Commands

 **BUY**: Buy an amount of stocks. Syntax: `BUY <stock_symbol> <amount> <price_per_stock> <user_id>`
- **SELL**: Sell an amount of stocks. Syntax: `SELL <stock_symbol> <amount> <price_per_stock> 

## Files
Descriptions of `server.py` and `client.py`, explaining their roles in the application.

## Command Usage

- **BUY**: `BUY MSFT 3.4 1.35 1`
- **SELL**: `SELL APPL 2 1.45 1`
- **LIST**: `LIST`
- **BALANCE**: `BALANCE`
- **SHUTDOWN**: `SHUTDOWN`

## Response Codes

- **200 OK**: Operation successful.
- **400 invalid command**: Invalid command received.
- **403 message format error**: Message format error.
- **404 stock not found**: Stock symbol not found.
- **405 not enough stock balance**: Not enough stock balance.
