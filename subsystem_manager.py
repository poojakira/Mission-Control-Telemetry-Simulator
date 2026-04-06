# subsystem_manager.py - Satellite power and thermal subsystem simulation

SOLAR_CONSTANT = 1361.0  # W/m^2


class PowerThermalSubsystem:
    """Simulates satellite power generation, battery, and thermal state."""

    def __init__(self):
        self.battery_capacity = 80.0
        self.current_charge = 80.0
        self.solar_efficiency = 0.28
        self.solar_area = 0.12
        self.base_load = 5.0
        self.heater_load = 12.0
        self.thruster_load = 45.0
        self.temperature = 20.0

    def update(self, dt, is_eclipse, is_thrusting):
        generation = 0.0
        if not is_eclipse:
            generation = SOLAR_CONSTANT * self.solar_area * self.solar_efficiency

        consumption = self.base_load
        if is_thrusting:
            consumption += self.thruster_load
        if is_eclipse:
            consumption += self.heater_load
            self.temperature -= (0.5 * dt)
        else:
            self.temperature += (0.2 * dt)

        net_power = generation - consumption
        energy_step = net_power * (dt / 3600.0)
        self.current_charge += energy_step
        self.current_charge = max(0.0, min(self.current_charge, self.battery_capacity))

        return {
            'charge_pct': (self.current_charge / self.battery_capacity) * 100,
            'temp_c': self.temperature,
            'power_draw': consumption,
        }

    def simulate_cycle(self, dt=1.0, is_eclipse=False, is_thrusting=False):
        return self.update(dt=dt, is_eclipse=is_eclipse, is_thrusting=is_thrusting)
