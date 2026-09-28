import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket()
client.connect((HOST, PORT))

print("Welcome to FAST-NUCES Karachi Campus CGPA Calculator!")

student_id = input("Enter Student ID: ")
n = int(input("Enter number of subjects: "))

data = [student_id, str(n)]

for i in range(n):
    credit = input(f"Enter credit hours for Subject {i + 1}: ")
    marks = input(f"Enter marks for Subject {i + 1}: ")

    data.append(credit)
    data.append(marks)

message = ",".join(data)
client.send(message.encode())

result = client.recv(4096).decode()

print("\n" + result)

client.close()