
# Three-Body Problem Simulation with Real-Time Visualization

This project is a Python simulation of the **Three-Body Problem** with real-time visualization using `matplotlib` and `scipy`. The simulation models three stars and a habitable planet, showing their gravitational interactions and dynamic orbits. You can restart the simulation with randomized initial conditions by pressing `Ctrl-R`.

## Features
- Real-time simulation and visualization of the Three-Body Problem.
- Adaptive time-stepping with improved solver accuracy.
- Dynamic plot centering to follow the stars and planet during their motion.
- Supports restarting the simulation with new random initial conditions using a keypress (`Ctrl-R`).
  
## The Three-Body Problem
The three-body problem is a classic physics problem where the motion of three masses is governed by Newton's laws of motion and gravitation. Due to the chaotic nature of the system, there is no general analytical solution, and it must be solved numerically.

In this simulation:
- Three stars of equal mass interact gravitationally.
- A habitable planet orbits within the system, also subject to the gravitational forces of the stars.
- The simulation provides a real-time display of the stars and the planet as they move.

## Installation

### Prerequisites
- **Python 3.8+**
- **pip** (Python package installer)

### Required Libraries
To install the required libraries, run:

```bash
pip install numpy scipy matplotlib
```

### Clone the Repository
To get started, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/three-body-simulation.git
cd three-body-simulation
```

## Running the Simulation
To run the simulation, simply execute the Python script:

```bash
python ThreeBody.py
```

You will see a dynamic visualization of the stars and the planet. The plot will auto-center to follow the motion of the celestial bodies.

### Controls
- **Ctrl-R**: Restart the simulation with randomized initial conditions.

## Code Overview

### `ThreeBody.py`
This is the main script that:
- Sets up the simulation using `scipy.integrate.solve_ivp` for solving the equations of motion.
- Handles real-time plotting and visualization using `matplotlib.animation`.
- Implements gravitational interactions between the stars and the planet, with adaptive solver tolerances for numerical stability.

### Key Components:
1. **`equations_of_motion`**: Defines the accelerations due to gravitational forces for each body.
2. **`solve_ivp`**: Solves the system of differential equations numerically.
3. **`FuncAnimation`**: Handles the real-time update of the plot.
4. **Key Bindings**: Detects the `Ctrl-R` key combination to restart the simulation.

### Adaptive Solver
We use an adaptive Runge-Kutta method (`RK45`) with tight tolerance settings (`rtol=1e-8` and `atol=1e-10`) to ensure numerical stability during close encounters between stars.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contribution
Feel free to fork the project and submit pull requests if you have improvements, bug fixes, or new features you'd like to add.

## Acknowledgments
This project was built using the following libraries:
- [NumPy](https://numpy.org/) - For numerical operations.
- [SciPy](https://www.scipy.org/) - For solving differential equations.
- [Matplotlib](https://matplotlib.org/) - For real-time visualization.
