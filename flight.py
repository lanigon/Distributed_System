class Flight:
    def __init__(self=None, ID=None, source=None, destination=None, departure_time=None, seat_availability=None, duration=None):
        self.ID = ID
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.seat_availability = seat_availability
        self.duration = duration

class receivedFlight:
    def __init__(self=None, ID=None, source=None, destination=None, departure_time=None, airfare=None, seat_availability=None, ):
        self.ID = ID
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.seat_availability = seat_availability
        self.airfare = airfare