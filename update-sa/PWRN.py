import socket
import threading

PORTS = [8486, 6669, 6612, 1230, 2044, 8044]
RESPONSE = b"FEJP"

def handle_client(conn, addr):
    try:
        conn.recv(1024)
        conn.sendall(RESPONSE)
    except:
        pass
    finally:
        conn.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", port))
    server.listen(5)
    while True:
        try:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except:
            continue

for port in PORTS:
    threading.Thread(target=start_server, args=(port,), daemon=True).start()

threading.Event().wait()
