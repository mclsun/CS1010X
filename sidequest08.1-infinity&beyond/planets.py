from math import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import integrate
from scipy.constants import physical_constants

# Define representation of a planet
def make_planet(x_pos, y_pos, mass, colour, size):
    return (x_pos, y_pos, mass, colour, size)

def get_x_coordinate(planet):
    return planet[0]

def get_y_coordinate(planet):
    return planet[1]

def get_mass(planet):
    return planet[2]

def get_colour(planet):
    return planet[3]

def get_size(planet):
    return planet[4]

def get_position(planet):
    return (get_x_coordinate(planet), get_y_coordinate(planet))

# Setup constants
G = physical_constants['Newtonian constant of gravitation'][0]
Mass_of_Earth = 6 * 10**24
Earth = make_planet(0, 0, Mass_of_Earth / 10**13, 'ob', 16)
Mars = make_planet(0.5, 0.7, 0.1 * Mass_of_Earth / 10**13, 'or', 20)
Moon = make_planet(0.03, 0.1, 7.348 * 10 ** 22 / 10**13, 'oy', 8)

# Scaling factor for the graph
unit = 10**13

# Drawing the environment of the simulation
fig = plt.figure()
axes = plt.axes(xlim=(-0.2, 1), ylim=(-0.5, 1.5))
line, = axes.plot([], [], lw=2)


def planet_plot(planets_list):
    for planet in planets_list:
        axes.plot(get_x_coordinate(planet), get_y_coordinate(planet), get_colour(planet), markersize=get_size(planet))


def plot_planets(planets_list, dest_planet):
    circle = plt.Circle(get_position(dest_planet), 0.1)
    circle.fill = False
    axes.add_artist(circle)
    planet_plot(planets_list)


def setup_spacecraft(vx, vy, f):
    # Initial Time
    t0 = 0

    # Iteration speed
    dt = 0.001

    # Vector with the spacecraft's initial position and speed
    y0 = np.array([0, 0.1, vx, vy])

    # Set up of the integrator to iterate the parameters of the spacecraft
    integrator = integrate.ode(f).set_integrator('dopri5', atol=1e-6)
    integrator.set_initial_value(y0, t0)

    #initial animation state
    pause = False

    # This function will plot out the path of the spacecrat
    def animate(i):
        nonlocal pause
        if not pause:
            integrator.integrate(integrator.t+dt)
            current_x = integrator.y[0]
            current_y = integrator.y[1]
            if (current_x < 0.0 and current_y < 0.0) or (0.46 < current_x < 0.54 and 0.66 < current_y < 0.74):
                pause = True
            else:
                axes.scatter(current_x, current_y, s=5)

    #setup matplotlib's animator
    return animation.FuncAnimation(fig, animate, interval=10, blit=False)


def start_spacecraft_animation(initial_vx, initial_vy, f):
    anim = setup_spacecraft(initial_vx, initial_vy, f)
    plt.show()
