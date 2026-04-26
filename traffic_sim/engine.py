import random
import networkx as nx
from .components import Vehicle, Road, Junction, Source, Sink

class Simulator:
    def __init__(self):
        self.G = nx.DiGraph() # Used for pathfinding and visualization structure
        self.junctions = {}
        self.roads = {}
        self.sources = []
        self.sinks = {}
        self.vehicles = []
        self.time = 0
        self.vehicle_counter = 0
        # Colors assigned to destinations for visual distinction
        self.colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']

    def add_junction(self, node_id, pos):
        self.junctions[node_id] = Junction(node_id)
        self.G.add_node(node_id, pos=pos)

    def add_road(self, u, v, capacity=10, travel_time=5):
        road = Road(u, v, capacity, travel_time)
        self.roads[(u, v)] = road
        self.junctions[u].out_roads.append(road)
        self.junctions[v].in_roads.append(road)
        self.G.add_edge(u, v)

    def add_source(self, node_id, rate, destinations):
        self.sources.append(Source(node_id, rate, destinations))

    def add_sink(self, node_id):
        self.sinks[node_id] = Sink(node_id)

    def step(self):
        # 1. GENERATE TRAFFIC: Sources create vehicles
        for src in self.sources:
            if random.random() < src.rate:
                dst = random.choice(src.destinations)
                try:
                    # Find shortest path via NetworkX
                    path = nx.shortest_path(self.G, src.node_id, dst)
                    if len(path) > 1:
                        color = self.colors[hash(dst) % len(self.colors)]
                        v = Vehicle(self.vehicle_counter, src.node_id, dst, path, self.time, color)
                        
                        first_road = self.roads[(path[0], path[1])]
                        # Check road capacity before spawning
                        if len(first_road.moving_vehicles) + len(first_road.queue) < first_road.capacity:
                            v.current_road = first_road
                            first_road.moving_vehicles.append(v)
                            self.vehicles.append(v)
                            self.vehicle_counter += 1
                except nx.NetworkXNoPath:
                    pass

        # 2. MOVE VEHICLES: Advance vehicles along roads
        for road in self.roads.values():
            arrived = []
            for v in road.moving_vehicles:
                v.progress += 1.0 / road.travel_time
                if v.progress >= 1.0:
                    v.progress = 1.0
                    arrived.append(v)
            # Move arrived vehicles into the junction queue
            for v in arrived:
                road.moving_vehicles.remove(v)
                road.queue.append(v)

        # 3. SCHEDULE JUNCTIONS: Process queues
        for j in self.junctions.values():
            if not j.in_roads: continue
            
            # Simple Round-Robin Scheduling: allow 1 vehicle to pass per tick per junction
            start_idx = j.rr_index
            for _ in range(len(j.in_roads)):
                j.rr_index = (j.rr_index + 1) % len(j.in_roads)
                road = j.in_roads[j.rr_index]
                
                if road.queue:
                    v = road.queue[0]
                    v.path_idx += 1
                    
                    # Check if reached the end of the path (Sink)
                    if v.path_idx == len(v.path) - 1:
                        if v.destination in self.sinks:
                            road.queue.popleft()
                            v.end_time = self.time
                            self.sinks[v.destination].absorbed += 1
                            self.sinks[v.destination].travel_times.append(v.end_time - v.start_time)
                            self.vehicles.remove(v)
                            break
                    else:
                        # Move to the next road in path
                        next_node = v.path[v.path_idx + 1]
                        next_road = self.roads[(v.path[v.path_idx], next_node)]
                        
                        # Respect next road's capacity
                        if len(next_road.moving_vehicles) + len(next_road.queue) < next_road.capacity:
                            road.queue.popleft()
                            v.current_road = next_road
                            v.progress = 0.0
                            next_road.moving_vehicles.append(v)
                            break
                            
        self.time += 1