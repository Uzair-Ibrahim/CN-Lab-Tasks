import socket
import random
import struct

dns_server = input("Enter DNS Server IP: ")
port = 53

while True:

    domain = input("\nEnter domain name (or type exit): ")

    if domain.lower() == "exit":
        break

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    print("\nDNS Server:", dns_server)
    print("Port:", port)
    print("Domain:", domain)

    def encode_domain(domain):
        result = b""

        for part in domain.split("."):
            result += bytes([len(part)]) + part.encode()

        return result + b"\x00"

    try:
        encoded_domain = encode_domain(domain)

        transaction_id = random.randint(0, 65535)
        flags = 0x0100

        qdcount = 1
        ancount = 0
        nscount = 0
        arcount = 0

        header = struct.pack(
            "!HHHHHH",
            transaction_id,
            flags,
            qdcount,
            ancount,
            nscount,
            arcount
        )

        qtype = 1
        qclass = 1

        question = encoded_domain + struct.pack("!HH", qtype, qclass)

        query = header + question

        sock.sendto(query, (dns_server, port))

        print("DNS query sent.")

        response, server_address = sock.recvfrom(512)

        print("Response received.")

        if len(response) < 12:
            print("Malformed DNS response.")
            sock.close()
            continue

        response_header = struct.unpack("!HHHHHH", response[:12])

        response_transaction_id = response_header[0]
        response_flags = response_header[1]
        question_count = response_header[2]
        answer_count = response_header[3]
        authority_count = response_header[4]
        additional_count = response_header[5]

        print("Transaction ID:", response_transaction_id)
        print("Flags:", hex(response_flags))
        print("Question Count:", question_count)
        print("Answer Count:", answer_count)

        if response_transaction_id != transaction_id:
            print("Invalid DNS response.")
            sock.close()
            continue

        rcode = response_flags & 0x000F

        if rcode == 3:
            print("NXDOMAIN: Domain does not exist.")
            sock.close()
            continue

        if answer_count == 0:
            print("No answer found.")
            sock.close()
            continue

        offset = 12

        for i in range(question_count):
            while response[offset] != 0:
                offset += 1

            offset += 1
            offset += 4

        for i in range(answer_count):

            if response[offset] & 0xC0 == 0xC0:
                offset += 2
            else:
                while response[offset] != 0:
                    offset += 1
                offset += 1

            record_type = struct.unpack(
                "!H", response[offset:offset + 2]
            )[0]
            offset += 2

            record_class = struct.unpack(
                "!H", response[offset:offset + 2]
            )[0]
            offset += 2

            ttl = struct.unpack(
                "!I", response[offset:offset + 4]
            )[0]
            offset += 4

            data_length = struct.unpack(
                "!H", response[offset:offset + 2]
            )[0]
            offset += 2

            if record_type == 1 and data_length == 4:
                ip_address = socket.inet_ntoa(
                    response[offset:offset + 4]
                )

                print("IP Address:", ip_address)
                print("TTL:", ttl)

            offset += data_length

    except socket.timeout:
        print("DNS request timed out.")

    except socket.gaierror:
        print("Invalid DNS server IP.")

    except Exception as e:
        print("Error:", e)

    finally:
        sock.close()

print("Program ended.")
