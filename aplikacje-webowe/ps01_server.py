import socket


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Nasłuchuję na http://{host}:{port}")

    while True:
        conn, addr = server.accept()
        request = conn.recv(1024).decode()
        request_lines = request.splitlines()

        for line in request_lines:
            print(line)

        parts = request_lines[0].split()
        method = parts[0]
        path = parts[1]

        status = "HTTP/1.1 200 OK"
        if path == "/":
            if method == "GET":
                body = "Witaj!"
            else:
                status = "HTTP/1.1 405 Method Not Allowed"
                body = "Dozwolona tylko metoda GET"
        elif path == "/info":
            if method == "GET":
                body = "Witaj na podstronie /info!"
            else:
                status = "HTTP/1.1 405 Method Not Allowed"
                body = "Dozwolona tylko metoda GET"
        else:
            status = "HTTP/1.1 404 Not Found"
            body = "Nie wykryto takiej ścieżki"

        response = (
            f"\n{status}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            f"\r\n{body}"
        )

        conn.sendall(response.encode())
        conn.close()


start_server("127.0.0.1", 8080)