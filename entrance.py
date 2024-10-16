import cmd
import socket
from flight import Flight
from serialization import serialize_flight, deserialize_flights
import struct
from datetime import datetime

class MyCmdApp(cmd.Cmd):
    intro = 'Welcome to the DS Flight System. Type help or ? to list commands.\n'
    prompt = '(DS Flight System) '

    def __init__(self):
        super().__init__()
        self.ipadd = '192.168.1.53'
        self.port = 8080
        self.username = ""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(5.0)
        self.buffer_size = 4096
        self.maxtimes = 5

    def preloop(self):
        while self.username == "":
            self.register(input('Please enter your username: '))
    
    def register(self, arg):
        """Please enter you username"""
        if(arg == "" or (len(arg.split()) != 1)):
            print("Please enter your username")
        else:
            self.username = arg

    # def do_hello(self, arg):
    #     """Say hello: hello <name>"""
    #     print(f"Hello {self.username}")

    def do_exit(self, arg):
        """Exit the command line"""
        print("Goodbye!")
        return True

    def do_enquiryByPoint(self, arg):
        """Enquiry flight information by start and end points: enquiryByPoint <start> <end>"""
        args = arg.split()
        if len(args) != 2:
            print("Error: Please provide exactly two arguments: <start> <end>. Usage: enquiryByPoint <start> <end>")
            return
        start, end = args

        print(f"Enquiring flight from {start} to {end}...")
        flight = Flight(
            ID=0,
            source=start,
            destination=end,
            departure_time="",
            seat_availability=150,
            duration= 0
        )
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        current_time = datetime.now()
        timestamp = current_time.timestamp()
        serialized_data = serialize_flight(flight, 1, timestamp, ip_address)

        self.client_socket.sendto(serialized_data, (self.ipadd, self.port))
        retries = 0
        while(retries < self.maxtimes):
          try:
              data, server = self.client_socket.recvfrom(4096)
              status, opcode, flights, message = deserialize_flights(data)
              print(message)
              for flight in flights:
                print("ID:"+str(flight.ID))
                print("source:"+flight.source)
                print("destination:"+flight.destination)
                print("departure_time:"+flight.departure_time)
                print("airfare:"+str(flight.airfare))
                print("seat_availability:"+str(flight.seat_availability))
              break
          except socket.timeout:
              retries += 1
              print(f"Request timed out. Retrying {retries}/{max_retries}...")
              if retries >= max_retries:
                  print("Max retries reached. Request failed.")
                  break

    def do_enquiryByID(self, arg):
        """Enquiry flight information by flight ID: enquiryByID <flight_id>"""
        args = arg.split()
        if len(args) != 1:
            print("Error: Please provide exactly one argument: <flight_id>. Usage: enquiryByID <flight_id>")
            return

        flight_id = args[0]

        try:
            flight_id = int(flight_id)
            print(f"Enquiring flight information for ID {flight_id}...")

        except ValueError:
            print("Error: Flight ID must be an integer. Usage: enquiryByID <flight_id>")
            return
        
        flight = Flight(
            ID=flight_id,
            source="",
            destination="",
            departure_time="",
            seat_availability=150,
            duration= 0
        )
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        current_time = datetime.now()
        timestamp = current_time.timestamp()
        serialized_data = serialize_flight(flight, 2, timestamp, ip_address)
        retries = 0
        while(retries < self.maxtimes):
          try:
              self.client_socket.sendto(serialized_data, (self.ipadd, self.port))
              data, server = self.client_socket.recvfrom(4096)
              status, opcode, flights, message = deserialize_flights(data)
              print(message)
              for flight in flights:
                print("ID:"+str(flight.ID))
                print("source:"+flight.source)
                print("destination:"+flight.destination)
                print("departure_time:"+flight.departure_time)
                print("airfare:"+str(flight.airfare))
                print("seat_availability:"+str(flight.seat_availability))
              break
          except socket.timeout:
              retries += 1
              print(f"Request timed out. Retrying {retries}/{max_retries}...")
              if retries >= max_retries:
                  print("Max retries reached. Request failed.")
                  break

    def do_monitor(self, arg):
        """Monitor flight status: monitor <flight_id> <monitor_time>"""
        args = arg.split()
        if len(args) != 2:
            print("Error: Please provide exactly one argument: <flight_id>. Usage: monitor <flight_id>")
        flight_id = args[0]
        time = args[1]
        
        try:
            flight_id = int(flight_id)
            flight = Flight(
                ID=flight_id,
                source="",
                destination="",
                departure_time="",
                seat_availability=150,
                duration= time
            )
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            current_time = datetime.now()
            timestamp = current_time.timestamp()
            serialized_data = serialize_flight(flight, 4, timestamp, ip_address)
            self.client_socket.sendto(serialized_data, (self.ipadd, self.port))
            print(f"Monitoring flight {flight_id}...")
            while True:
              buffer_size = 1024
              try:
                  data, server_address = self.client_socket.recvfrom(buffer_size)
                  status, opcode, flights, message = deserialize_flights(data)
                  print(message)

              except socket.timeout:
                  continue
        except ValueError:
            print("Error: Flight ID must be an integer. Usage: monitor <flight_id>")
    
    def do_enquiryScores(self, arg):
        """Enquiry scores: enquiryScores"""
        flight = Flight(
            ID=110,
            source="",
            destination="",
            departure_time="",
            seat_availability=150,
            duration= 0
        )
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        current_time = datetime.now()
        timestamp = current_time.timestamp()
        serialized_data = serialize_flight(flight, 5, timestamp, ip_address)
        retries = 0
        while(retries < self.maxtimes):
          try:
              self.client_socket.sendto(serialized_data, (self.ipadd, self.port))
              data, server_address = self.client_socket.recvfrom(self.buffer_size)
              status, opcode, flights, message = deserialize_flights(data)
              print(message)
              break
          except socket.timeout:
              retries += 1
              print(f"Request timed out. Retrying {retries}/{max_retries}...")
              if retries >= max_retries:
                  print("Max retries reached. Request failed.")
                  break

    def do_reserveSeat(self, arg):
        """Reserve a seat on a flight: reserveSeat <flight_id>"""
        args = arg.split()
        if len(args) != 2:
            print("Error: Please provide exactly one arguments: <flight_id>. Usage: reserveSeat <flight_id> <seat_count>")
            return

        flight_id = args[0]
        count = args[1]
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        current_time = datetime.now()
        timestamp = current_time.timestamp()
        retries = 0
        while(retries < self.maxtimes):
          try:
              flight_id = int(flight_id)
              flight = Flight(
                  ID= flight_id,
                  source="",
                  destination="",
                  departure_time="",
                  seat_availability= count,
                  duration= 0
              )
              serialized_data = serialize_flight(flight, 3, timestamp, ip_address)
              self.client_socket.sendto(serialized_data, (self.ipadd, self.port))
              data, server = self.client_socket.recvfrom(4096)
              status, opcode, flights, message = deserialize_flights(data)
              print(message)
              seat_count = flights
              break

          except ValueError as e:
              print(f"Error: {e}. Usage: reserveSeat <flight_id> ")
          except socket.timeout:
              retries += 1
              print(f"Request timed out. Retrying {retries}/{max_retries}...")
              if retries >= max_retries:
                  print("Max retries reached. Request failed.")
                  break


    def do_quit(self, arg):
        """Exit the command line"""

if __name__ == '__main__':
    MyCmdApp().cmdloop()
