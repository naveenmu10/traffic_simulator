import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx

class Visualizer:
    def __init__(self, sim):
        self.sim = sim
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.pos = nx.get_node_attributes(sim.G, 'pos')

    def animate(self, frame):
        self.sim.step()
        self.ax.clear()
        self.ax.set_title(f"Network Traffic Simulator - Time Step: {self.sim.time}")

        # Draw static network (Junctions and Roads)
        nx.draw_networkx_nodes(self.sim.G, self.pos, ax=self.ax, node_color='lightgray', node_size=600)
        nx.draw_networkx_edges(self.sim.G, self.pos, ax=self.ax, edge_color='gray', arrows=True, arrowsize=15)
        nx.draw_networkx_labels(self.sim.G, self.pos, ax=self.ax, font_weight='bold')

        # Draw moving vehicles
        if self.sim.vehicles:
            x, y, colors = [], [], []
            for v in self.sim.vehicles:
                u_pos = self.pos[v.current_road.start_node]
                v_pos = self.pos[v.current_road.end_node]
                
                # Interpolate position based on progress (0.0 to 1.0)
                vx = u_pos[0] + (v_pos[0] - u_pos[0]) * v.progress
                vy = u_pos[1] + (v_pos[1] - u_pos[1]) * v.progress
                x.append(vx)
                y.append(vy)
                colors.append(v.color)
            
            # Render vehicles as colored scatter points
            self.ax.scatter(x, y, c=colors, s=120, zorder=5, edgecolors='black')

        # Display Live Statistics on the plot
        stats = "Stats (Absorbed):\n"
        for s_id, sink in self.sim.sinks.items():
            avg_time = sum(sink.travel_times) / len(sink.travel_times) if sink.travel_times else 0
            stats += f"Sink {s_id}: {sink.absorbed} (Avg Time: {avg_time:.1f})\n"
            
        self.ax.text(0.02, 0.98, stats, transform=self.ax.transAxes, va='top', 
                     bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'))

    def save_gif(self, filename="simulation.gif", frames=150, fps=10):
        ani = animation.FuncAnimation(self.fig, self.animate, frames=frames, interval=1000/fps)
        ani.save(filename, writer='pillow')
        plt.close()
        print(f"Visualization saved to {filename}")