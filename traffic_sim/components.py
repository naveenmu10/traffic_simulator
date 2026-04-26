from collections import deque

class Vehicle:
    def __init__(self, v_id, source, destination, path, start_time, color):
        self.v_id = v_id
        self.source = source
        self.destination = destination
        self.path = path          # List of node IDs forming the route
        self.path_idx = 0         # Current position in the path list
        self.start_time = start_time
        self.end_time = None
        self.color = color        # Visualization color based on destination
        self.current_road = None
        self.progress = 0.0       # 0.0 to 1.0 representing travel along the road

class Road:
    def __init__(self, start_node, end_node, capacity, travel_time):
        self.start_node = start_node
        self.end_node = end_node
        self.capacity = capacity
        self.travel_time = travel_time
        self.moving_vehicles = [] # Vehicles currently driving on the road
        self.queue = deque()      # Vehicles waiting at the end of the road (junction queue)

class Junction:
    def __init__(self, node_id):
        self.node_id = node_id
        self.in_roads = []
        self.out_roads = []
        self.rr_index = 0         # Used for Round-Robin scheduling

class Source:
    def __init__(self, node_id, rate, destinations):
        self.node_id = node_id
        self.rate = rate          # Probability of generating a vehicle per tick (Poisson-like)
        self.destinations = destinations

class Sink:
    def __init__(self, node_id):
        self.node_id = node_id
        self.absorbed = 0
        self.travel_times = []