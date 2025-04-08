# water_flow.py

import math

EARTH_ACCELERATION_OF_GRAVITY = 9.80665
WATER_DENSITY = 998.2
WATER_DYNAMIC_VISCOSITY = 0.0010016

def water_column_height(tower_height, tank_height):
    """Calculates and returns the height of water in a column.

    Parameters:
        tower_height: The height of the water tower in meters.
        tank_height: The height of the tank walls in meters.

    Return:
        The height of the water column in meters.
    """
    return tower_height + (3 * tank_height) / 4

def pressure_gain_from_water_height(height):
    """Calculates and returns the pressure gained from the height of a column of water.

    Parameters:
        height: The height of the water column in meters.

    Return:
        The pressure gained in kilopascals.
    """
    return (WATER_DENSITY * EARTH_ACCELERATION_OF_GRAVITY * height) / 1000

def pressure_loss_from_pipe(diameter, length, friction, velocity):
    """Calculates and returns the water pressure lost from water flowing
    through a pipe.

    Parameters:
        diameter: The diameter of the pipe in meters.
        length: The length of the pipe in meters.
        friction: The friction factor of the pipe.
        velocity: The velocity of the water in meters per second.

    Return:
        The lost pressure in kilopascals.
    """
    return -friction * length * WATER_DENSITY * (velocity**2) / (2000 * diameter)

def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """Calculates and returns the water pressure lost from fittings.

    Parameters:
        fluid_velocity: The velocity of the water in meters per second.
        quantity_fittings: The quantity of fittings.

    Return:
        The lost pressure in kilopascals.
    """
    return -0.04 * WATER_DENSITY * (fluid_velocity**2) * quantity_fittings / 2000

def reynolds_number(hydraulic_diameter, fluid_velocity):
    """Calculates and returns the Reynolds number for a pipe.

    Parameters:
        hydraulic_diameter: The hydraulic diameter of the pipe in meters.
        fluid_velocity: The velocity of the water in meters per second.

    Return:
        The Reynolds number.
    """
    return (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / WATER_DYNAMIC_VISCOSITY

def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    """Calculates and returns the water pressure lost from pipe reduction.

    Parameters:
        larger_diameter: The diameter of the larger pipe in meters.
        fluid_velocity: The velocity of the water in meters per second.
        reynolds_number: The Reynolds number.
        smaller_diameter: The diameter of the smaller pipe in meters.

    Return:
        The lost pressure in kilopascals.
    """
    k = (0.1 + (50 / reynolds_number)) * ((larger_diameter / smaller_diameter)**4 - 1)
    return -k * WATER_DENSITY * (fluid_velocity**2) / 2000

def kpa_to_psi(kpa):
    """Converts kilopascals to pounds per square inch."""
    return kpa * 0.145038

PVC_SCHED80_INNER_DIAMETER = 0.28687  # (meters)  11.294 inches
PVC_SCHED80_FRICTION_FACTOR = 0.013  # (unitless)
SUPPLY_VELOCITY = 1.65  # (meters / second)
HDPE_SDR11_INNER_DIAMETER = 0.048692  # (meters)  1.917 inches
HDPE_SDR11_FRICTION_FACTOR = 0.018  # (unitless)
HOUSEHOLD_VELOCITY = 1.75  # (meters / second)

def main():
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))

    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)

    diameter = PVC_SCHED80_INNER_DIAMETER
    friction = PVC_SCHED80_FRICTION_FACTOR
    velocity = SUPPLY_VELOCITY
    reynolds = reynolds_number(diameter, velocity)

    loss = pressure_loss_from_pipe(diameter, length1, friction, velocity)
    pressure += loss

    loss = pressure_loss_from_fittings(velocity, quantity_angles)
    pressure += loss

    loss = pressure_loss_from_pipe_reduction(diameter, velocity, reynolds, HDPE_SDR11_INNER_DIAMETER)
    pressure += loss

    diameter = HDPE_SDR11_INNER_DIAMETER
    friction = HDPE_SDR11_FRICTION_FACTOR
    velocity = HOUSEHOLD_VELOCITY

    loss = pressure_loss_from_pipe(diameter, length2, friction, velocity)
    pressure += loss

    psi_pressure = kpa_to_psi(pressure)

    print(f"Pressure at house: {pressure:.1f} kilopascals")
    print(f"Pressure at house: {psi_pressure:.1f} psi")

if __name__ == "__main__":
    main()