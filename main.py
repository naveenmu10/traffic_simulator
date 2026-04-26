from traffic_sim.engine import Simulator
from traffic_sim.visualizer import Visualizer

def main():
    # 1. Initialize Simulator
    sim = Simulator()

    # 2. Define Network Topology (Coordinates are for visualization layout)
    # Using a planar network with < 10 junctions as required
    sim.add_junction('J1', pos=(0, 2))
    sim.add_junction('J2', pos=(2, 2))
    sim.add_junction('J3', pos=(2, 0))
    sim.add_junction('J4', pos=(0, 0))
    sim.add_junction('J5', pos=(1, 1)) # Central Hub (e.g., 4-way intersection)

    # 3. Add Directional Roads (Start, End, Capacity, Travel Time)
    sim.add_road('J1', 'J2', capacity=6, travel_time=4)
    sim.add_road('J2', 'J3', capacity=6, travel_time=4)
    sim.add_road('J3', 'J4', capacity=6, travel_time=4)
    sim.add_road('J4', 'J1', capacity=6, travel_time=4)
    
    # Inner crossroads connecting to the hub
    sim.add_road('J1', 'J5', capacity=3, travel_time=2)
    sim.add_road('J5', 'J3', capacity=3, travel_time=2)
    sim.add_road('J2', 'J5', capacity=3, travel_time=2)
    sim.add_road('J5', 'J4', capacity=3, travel_time=2)

    # 4. Add Traffic Sources and Sinks
    sim.add_source('J1', rate=0.4, destinations=['J3', 'J4'])
    sim.add_source('J2', rate=0.3, destinations=['J4'])
    sim.add_sink('J3')
    sim.add_sink('J4')

    # 5. Run & Generate Visualization (.gif)
    print("Starting simulation and generating visualization. Please wait...")
    vis = Visualizer(sim)
    vis.save_gif('traffic_simulation.gif', frames=150, fps=10)

    # 6. Output Statistics
    print("\n--- Final Simulation Statistics ---")
    for s_id, sink in sim.sinks.items():
        avg_t = sum(sink.travel_times) / len(sink.travel_times) if sink.travel_times else 0
        print(f"Sink {s_id}: Absorbed {sink.absorbed} vehicles. Average Travel Time: {avg_t:.2f} ticks.")

if __name__ == '__main__':
    main()