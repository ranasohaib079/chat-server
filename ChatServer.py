import sys
import socket
import threading


clients = []
clients_lock = threading.Lock()

def server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', port))
        server_socket.listen()
        
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            clients_lock.acquire()
            clients.append(conn)
            clients_lock.release()
            client_thread.start()

def handle_client(conn):
    named = False
    sender_name = None
    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    clients_lock.acquire()
                    clients.remove(conn)
                    clients_lock.release()
                    break
                recv = data.decode()
                if not named:
                    sender_name = recv
                    named = True
                else:
                    message = f"{sender_name}: {recv}"
                    print(message)
                    broadcast(message, conn)
    except Exception as e:
        print(f"Error in handle_client: {e}")

def broadcast(message, sender_conn):
    for conn in clients:
        if conn != sender_conn:
            try:
                conn.send(message.encode('ASCII'))
            except Exception as e:
                print(f"Broadcasting error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid Args")
        sys.exit(1)
    else:
        port = int(sys.argv[1])
        server(port)

