import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Gravitational constant
G = 1

# Masses of the three stars and the habitable planet
m1, m2, m3 = 1.0, 1.0, 1.0  # Stars
m_planet = 0.001  # Habitable planet (mass much smaller)

# Define the acceleration function
def acceleration(pos1, pos2, mass):
    r = np.linalg.norm(pos2 - pos1)
    if r == 0:  # Avoid division by zero
        return np.zeros_like(pos1)
    return G * mass * (pos2 - pos1) / r**3

# Define the equations of motion
def equations_of_motion(t, y):
    # Unpack positions and velocities
    x1, y1, vx1, vy1 = y[0], y[1], y[2], y[3]
    x2, y2, vx2, vy2 = y[4], y[5], y[6], y[7]
    x3, y3, vx3, vy3 = y[8], y[9], y[10], y[11]
    x_p, y_p, vx_p, vy_p = y[12], y[13], y[14], y[15]

    # Position vectors
    r1 = np.array([x1, y1])
    r2 = np.array([x2, y2])
    r3 = np.array([x3, y3])
    r_p = np.array([x_p, y_p])

    # Accelerations due to gravitational forces
    a1 = acceleration(r1, r2, m2) + acceleration(r1, r3, m3)
    a2 = acceleration(r2, r1, m1) + acceleration(r2, r3, m3)
    a3 = acceleration(r3, r1, m1) + acceleration(r3, r2, m2)
    
    # Planet accelerations due to all three stars
    a_p = acceleration(r_p, r1, m1) + acceleration(r_p, r2, m2) + acceleration(r_p, r3, m3)

    # Derivatives (velocities and accelerations)
    derivatives = [vx1, vy1, a1[0], a1[1],
                   vx2, vy2, a2[0], a2[1],
                   vx3, vy3, a3[0], a3[1],
                   vx_p, vy_p, a_p[0], a_p[1]]

    return derivatives

# Randomize initial positions and velocities (x, y, vx, vy for each body)
def random_initial_conditions():
    return [
        np.random.uniform(-1, 1), np.random.uniform(-1, 1), np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5),  # Star 1
        np.random.uniform(-1, 1), np.random.uniform(-1, 1), np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5),  # Star 2
        np.random.uniform(-1, 1), np.random.uniform(-1, 1), np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5),  # Star 3
        np.random.uniform(-1, 1), np.random.uniform(-1, 1), np.random.uniform(-0.2, 0.2), np.random.uniform(-0.2, 0.2)   # Habitable planet
    ]

# Global variables to store animation and figure objects
ani = None
t_eval = np.linspace(0, 20, 1000)
fig, ax = plt.subplots(figsize=(8, 8))

def initialize_simulation():
    global x1_sol, y1_sol, x2_sol, y2_sol, x3_sol, y3_sol, x_p_sol, y_p_sol, ani, t_eval

    # Stop any existing animation before restarting
    if ani is not None:
        ani.event_source.stop()

    # Set initial conditions
    y0 = random_initial_conditions()

    # Solve the equations of motion using solve_ivp with improved tolerance
    sol = solve_ivp(equations_of_motion, (0, 20), y0, t_eval=t_eval, method='RK45', rtol=1e-8, atol=1e-10)

    # Extract positions from the solution
    x1_sol, y1_sol = sol.y[0], sol.y[1]
    x2_sol, y2_sol = sol.y[4], sol.y[5]
    x3_sol, y3_sol = sol.y[8], sol.y[9]
    x_p_sol, y_p_sol = sol.y[12], sol.y[13]

    # Reset the axis limits
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)

    # Reset line objects for the stars and the planet
    star1_line.set_data([], [])
    star2_line.set_data([], [])
    star3_line.set_data([], [])
    planet_line.set_data([], [])

    star1_traj.set_data([], [])
    star2_traj.set_data([], [])
    star3_traj.set_data([], [])
    planet_traj.set_data([], [])

    # Create the new animation
    ani = FuncAnimation(fig, update, frames=len(t_eval), init_func=init, blit=True, interval=50)

# Setup the figure and axis
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

# Create line objects for the stars and the planet
star1_line, = ax.plot([], [], 'o-', color='orange', label='Star 1', markersize=10)
star2_line, = ax.plot([], [], 'o-', color='yellow', label='Star 2', markersize=10)
star3_line, = ax.plot([], [], 'o-', color='red', label='Star 3', markersize=10)
planet_line, = ax.plot([], [], 'o-', color='blue', label='Planet', markersize=5)

# Create trajectory line objects for the stars and planet
star1_traj, = ax.plot([], [], '-', color='orange', linewidth=1)
star2_traj, = ax.plot([], [], '-', color='yellow', linewidth=1)
star3_traj, = ax.plot([], [], '-', color='red', linewidth=1)
planet_traj, = ax.plot([], [], '--', color='blue', linewidth=1)

# Initialize the plot objects
def init():
    star1_line.set_data([], [])
    star2_line.set_data([], [])
    star3_line.set_data([], [])
    planet_line.set_data([], [])
    
    star1_traj.set_data([], [])
    star2_traj.set_data([], [])
    star3_traj.set_data([], [])
    planet_traj.set_data([], [])
    
    return star1_line, star2_line, star3_line, planet_line, star1_traj, star2_traj, star3_traj, planet_traj

# Auto-center and update the plot limits
def update_limits(frame):
    x_positions = [x1_sol[frame], x2_sol[frame], x3_sol[frame], x_p_sol[frame]]
    y_positions = [y1_sol[frame], y2_sol[frame], y3_sol[frame], y_p_sol[frame]]
    
    center_x = np.mean(x_positions)
    center_y = np.mean(y_positions)
    
    max_distance = max(np.ptp(x_positions), np.ptp(y_positions))
    margin = 0.5  # Add some margin
    
    ax.set_xlim(center_x - max_distance/2 - margin, center_x + max_distance/2 + margin)
    ax.set_ylim(center_y - max_distance/2 - margin, center_y + max_distance/2 + margin)

# Animation function: update each frame
def update(frame):
    # Set the positions of the stars and planet for the current frame
    star1_line.set_data([x1_sol[frame]], [y1_sol[frame]])
    star2_line.set_data([x2_sol[frame]], [y2_sol[frame]])
    star3_line.set_data([x3_sol[frame]], [y3_sol[frame]])
    planet_line.set_data([x_p_sol[frame]], [y_p_sol[frame]])
    
    # Update the trajectory by keeping all previous points
    star1_traj.set_data(x1_sol[:frame], y1_sol[:frame])
    star2_traj.set_data(x2_sol[:frame], y2_sol[:frame])
    star3_traj.set_data(x3_sol[:frame], y3_sol[:frame])
    planet_traj.set_data(x_p_sol[:frame], y_p_sol[:frame])

    # Auto-center the view based on the current positions
    update_limits(frame)
    
    return star1_line, star2_line, star3_line, planet_line, star1_traj, star2_traj, star3_traj, planet_traj

# Key press event handler
def on_key_press(event):
    if event.key == 'ctrl+r':  # Detect Ctrl-R (platform-independent key combination)
        print("Ctrl-R detected! Restarting simulation...")
        initialize_simulation()

# Attach the key press event to the figure
fig.canvas.mpl_connect('key_press_event', on_key_press)

# Start the first simulation
initialize_simulation()

# Display the animation and plot
plt.legend()
plt.title('Real-Time Simulation of the Trisolaran System with Auto-Centering (Ctrl-R to Refresh)')
plt.grid(True)
plt.show()
