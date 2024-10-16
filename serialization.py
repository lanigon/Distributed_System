from flight import Flight, receivedFlight
import struct

def serialize_flight(flight: Flight, opcode: int, timestamp: str, ip_address: str) -> bytes:
    binary_data = struct.pack('B', opcode)

    id_encoded = str(flight.ID).encode('utf-8')
    binary_data += struct.pack('>B', len(id_encoded)) + id_encoded

    source_encoded = flight.source.encode('utf-8')
    binary_data += struct.pack('>B', len(source_encoded)) + source_encoded

    destination_encoded = flight.destination.encode('utf-8')
    binary_data += struct.pack('>B', len(destination_encoded)) + destination_encoded

    departure_time_encoded = flight.departure_time.encode('utf-8')
    binary_data += struct.pack('>B', len(departure_time_encoded)) + departure_time_encoded

    seat_availability_encoded = str(flight.seat_availability).encode('utf-8')
    binary_data += struct.pack('>B', len(seat_availability_encoded)) + seat_availability_encoded

    duration_encoded = str(flight.duration).encode('utf-8')
    binary_data += struct.pack('>B', len(duration_encoded)) + duration_encoded

    ip_and_timestamp = f"{ip_address} {timestamp}"
    ip_timestamp_encoded = ip_and_timestamp.encode('utf-8')
    binary_data += struct.pack('>B', len(ip_timestamp_encoded)) + ip_timestamp_encoded

    return binary_data

def deserialize_flights(binary_data: bytes):
    offset = 0

    statuscode = struct.unpack('B', binary_data[offset:offset + 1])[0]
    offset += 1

    opcode = struct.unpack('B', binary_data[offset:offset + 1])[0]
    offset += 1

    flight_count = struct.unpack('B', binary_data[offset:offset + 1])[0]
    offset += 1

    flights = []

    for _ in range(flight_count):
        flight, offset = deserialize_flight(binary_data, offset)
        flights.append(flight)

    message_len = struct.unpack('B', binary_data[offset:offset + 1])[0]
    offset += 1
    message = binary_data[offset:offset + message_len].decode('utf-8')

    return statuscode, opcode, flights, message


def deserialize_flight(binary_data: bytes, offset):

    id_len = struct.unpack('B', binary_data[offset:offset + 1])[0]
    offset += 1
    ID = int(binary_data[offset:offset + id_len].decode('utf-8'))
    offset += id_len

    source_len = struct.unpack('B', binary_data[offset:offset + 1])[0]
    offset += 1
    source = binary_data[offset:offset + source_len].decode('utf-8')
    offset += source_len

    destination_len = struct.unpack('B', binary_data[offset:offset + 1])[0]
    offset += 1
    destination = binary_data[offset:offset + destination_len].decode('utf-8')
    offset += destination_len

    departure_time_len = struct.unpack('B', binary_data[offset:offset + 1])[0]
    offset += 1
    departure_time = binary_data[offset:offset + departure_time_len].decode('utf-8')
    offset += departure_time_len

    airfare_len = struct.unpack('B', binary_data[offset:offset + 1])[0]
    offset += 1
    airfare = float(binary_data[offset:offset + airfare_len].decode('utf-8'))
    offset += airfare_len

    seat_availability_len = struct.unpack('B', binary_data[offset:offset + 1])[0]
    offset += 1
    seat_availability = int(binary_data[offset:offset + seat_availability_len].decode('utf-8'))
    offset += seat_availability_len

    flight = receivedFlight(ID, source, destination, departure_time, airfare, seat_availability)

    return flight, offset