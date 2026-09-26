import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(("127.0.0.1", 5000))
    while True:
        data = input()
        if data == "q":
            break
        client.sendall(data.encode())

        print(client.recv(1024).decode())
