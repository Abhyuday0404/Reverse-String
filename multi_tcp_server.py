import socket
import threading

def reverse_string(s):
    return s[::-1]

def handle_client(conn, addr):
    """Handle individual client connections"""
    print(f"New connection from {addr}")
    try:
        while True:
            data = conn.recv(10000).decode()
            if not data:
                break
            print(f"Received from {addr}: {data}")
            reversed_data = reverse_string(data)
            conn.sendall(reversed_data.encode())
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection closed for {addr}")

def start_server():
    HOST = '127.0.0.1'  # localhost
    PORT = 65432        # Port to listen on

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Multi-threaded TCP Server is listening on {HOST}:{PORT}")
        
        try:
            while True:
                conn, addr = s.accept()
                # Create a new thread for each client
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.daemon = True  # Thread will close when main program exits
                client_thread.start()
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_server()
