import socket
import threading


def handler(conn, addr):
    request = b""

    while b"\r\n\r\n" not in request:
        chunk = conn.recv(1024)
        if not chunk:
            break
        request += chunk

    # parser
    headers, body = request.split(b"\r\n\r\n", 1)
    headers_list = headers.decode().split("\r\n")
    request_line = headers_list[0].split()
    if len(request_line) < 2:
        method = None
        path = None
    else:
        method = request_line[0]
        path = request_line[1]

        head = {}
        for line in headers_list[1:]:
            key, value = line.split(":", 1)
            head[key.strip().lower()] = value.strip()

        content_length = int(head.get("content-length", 0))
        while len(body) < content_length:
            chunk = conn.recv(4096)
            if not chunk:
                break
            body += chunk

    # Tworzenie response
    if method is None:
        response = "HTTP/1.1 400 Bad Request\r\nConnection: close\r\n\r\nNiepoprawne żądanie"
        conn.sendall(response.encode())
        conn.close()
        return

    status = "HTTP/1.1 200 OK"
    extra = ""
    content = ""
    if path == "/":
        if method == "GET":
            content = "Witaj!"
        else:
            status = "HTTP/1.1 405 Method Not Allowed"
            extra = "Allow: GET\r\n"
    elif path == "/info":
        if method == "GET":
            content = "Witaj na podstronie /info!"
        else:
            status = "HTTP/1.1 405 Method Not Allowed"
            extra = "Allow: GET\r\n"
    elif path == "/echo":
        if method == "POST":
            content = body.decode()
        else:
            status = "HTTP/1.1 405 Method Not Allowed"
            extra = "Allow: POST\r\n"
    else:
        status = "HTTP/1.1 404 Not Found"
        content = "Nie wykryto takiej ścieżki"

    response = (
        f"\n{status}\r\n"
        f"{extra}"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(content)}\r\n"
        "Connection: close\r\n"
        f"\r\n{content}"
    )

    conn.sendall(response.encode())
    conn.close()


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Nasłuchuję na http://{host}:{port}")

    while True:
        conn, addr = server.accept()

        t = threading.Thread(target=handler, args=(conn, addr))
        t.start()


def main():
    host = input("Podaj hosta: ")
    port = int(input("Podaj port: "))
    start_server(host, port)


start_server("127.0.0.1", 8080)
#main()
