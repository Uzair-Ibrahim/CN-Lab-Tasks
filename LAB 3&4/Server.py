import socket

HOST = "127.0.0.1"
PORT = 5000

def get_gpa(marks):
    if marks >= 90:
        return 4.0
    elif marks >= 85:
        return 3.67
    elif marks >= 80:
        return 3.33
    elif marks >= 75:
        return 3.0
    elif marks >= 70:
        return 2.67
    elif marks >= 65:
        return 2.33
    elif marks >= 60:
        return 2.0
    elif marks >= 50:
        return 1.0
    else:
        return 0.0

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("Server is running...")
print("Waiting for client...")

conn, addr = server.accept()
print("Client connected.")

data = conn.recv(4096).decode()
parts = data.split(",")

student_id = parts[0]
n = int(parts[1])

total_points = 0
total_credits = 0

index = 2

for i in range(n):
    credit = float(parts[index])
    marks = float(parts[index + 1])
    index += 2

    gpa = get_gpa(marks)
    total_points += gpa * credit
    total_credits += credit

cgpa = total_points / total_credits

result = f"Student ID: {student_id}\nCGPA: {cgpa:.2f}"

conn.send(result.encode())

conn.close()
server.close()