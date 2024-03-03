import sys
import socket
import threading

clients = []
clients_lock = threading.Lock()

def client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            receive_thread.start()

            while True:
                try:
                    message = input()
                    if not message:
                        break
                    client_socket.send(message.encode('ASCII'))
                except EOFError:
                    break
                except KeyboardInterrupt:
                    print("\n")
                except Exception:
                    break
        except Exception as e:
            print(f"Error in client: {e}")
        finally:
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode())
        except ConnectionResetError:
            break
        except Exception as e:
            print("ERROR")
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid Args")
        sys.exit(1)
    else:
        port = int(sys.argv[1])
        host = socket.gethostbyname('localhost')
        client(host, port)

