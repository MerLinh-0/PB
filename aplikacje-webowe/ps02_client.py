import socket


def client(host, port, method, path, content):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        if method == "GET":
            extra = ""
        else:
            extra = f"Content-Length: {len(content)}\r\n"
            
        request = (
            f"\n{method} {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"{extra}"
            f"\r\n{content}"
        )
        client.sendall(request.encode())

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
            body = b""
            
        print(headers.decode())
        print()
        print(body.decode())
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        client.close()


def send_get_request():
    while True:
        host = input("Podaj hosta: ")
        port = int(input("Podaj port: "))
        method = input("Podaj metodę: ")
        path = input("Podaj ścieżkę: ")
        content = input("Podaj treść (opcjonalne): ")
        client(host, port, method, path, content)


send_get_request()
