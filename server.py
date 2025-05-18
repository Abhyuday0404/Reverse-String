import socket

def reverse_string(s):
    return s[::-1]

HOST = '127.0.0.1'  # localhost
PORT = 65432        # Port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received: {data}")
            reversed_data = reverse_string(data)
            conn.sendall(reversed_data.encode())


