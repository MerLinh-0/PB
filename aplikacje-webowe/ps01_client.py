import socket


def client(host, port, path):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.sendall(f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n".encode())

    response = b""
    while True:
        chunk = client.recv(4096)
        if not chunk:
            break
        response += chunk

    parts = response.split(b"\r\n\r\n", 1)
    headers = parts[0]
    if len(parts) > 1:
        body = parts[1]
    else:
        body = ""
        
    print(headers.decode())
    print()
    print(body.decode())
    client.close()


def send_get_request():
    host = input("Podaj hosta: ")
    port = int(input("Podaj port: "))
    path = input("Podaj ścieżkę: ")
    client(host, port, path)


send_get_request()
