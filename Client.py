import socket

SERVER_IP = "localhost"  # Change this to the server's IP address
SERVER_PORT = 7390  # Change this to the server's port

def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    client_socket.send(request.encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")
    print(f"Server response: {response}")
    client_socket.close()

def main():
    while True:
        command = input("Enter command (BUY/SELL/LIST/BALANCE/SHUTDOWN/QUIT): ").upper()

        if command == "QUIT":
            break

        if command not in ["BUY", "SELL", "LIST", "BALANCE", "SHUTDOWN"]:
            print("Invalid command")
            continue

        if command == "SHUTDOWN":
            confirm = input("Are you sure you want to shutdown the server? (yes/no): ").lower()
            if confirm != "yes":
                print("Shutdown aborted")
                continue

        request = input("Enter request: ")
        send_request(f"{command} {request}")

if __name__ == "__main__":
    main()