import socket

def reverse_string(s):
    return s[::-1]

HOST = '127.0.0.1'  # localhost
PORT = 65433        # Different port for UDP server

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"UDP Server is listening on {HOST}:{PORT}")
    while True:
        data, addr = s.recvfrom(10000)
        if not data:
            continue
        message = data.decode()
        print(f"Received from {addr}: {message}")
        reversed_data = reverse_string(message)
        s.sendto(reversed_data.encode(), addr)
