import socket
import config
from flight import Flight
from serialization import serialize_flight, deserialize_flights
import socket
from datetime import datetime

ipadd = '192.168.1.53'
port = 8080
def test():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    f = Flight(
        ID=110,
        source="",
        destination="",
        departure_time="",
        seat_availability=15,
        duration= 0
    )
    opcode = 2

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    current_time = datetime.now()
    timestamp = current_time.timestamp()

    serialized_data = serialize_flight(f, opcode, timestamp, ip_address)
    #(op,flight) = deserialize_flight(serialized_data)
    client_socket.sendto(serialized_data, (ipadd, port))
    data, server = client_socket.recvfrom(4096)
    print(f'Received: {data.decode()}')
    status, opcode, flights, message = deserialize_flights(data)
    print(status)
    print(opcode)
    print(flights[0].airfare)
    print(message)

    client_socket.sendto(serialized_data, (ipadd, port))
    data, server = client_socket.recvfrom(4096)
    status, opcode, flights, message = deserialize_flights(data)
    print(message)

try:
  test()
except Exception as e:
  print(e)