import numpy as np

# WGS84 Constants
MU = 398600.4418
R_EARTH = 6378.137


class ExtendedKalmanFilter:
    """
    Extended Kalman Filter for orbital state estimation.
    State vector: [x, y, z, vx, vy, vz] (position km, velocity km/s)
    """

    def __init__(self, initial_state, dt=1.0):
        self.state = initial_state.copy()
        self.dt = dt
        self.n = len(self.state)

        # Covariance matrix
        self.P = np.eye(self.n) * 1.0
        # Process noise
        self.Q = np.eye(self.n) * 0.0001
        # Measurement noise (default: full state measurement)
        self.R_pos = np.eye(3) * 0.5
        self.R_full = np.eye(self.n) * 0.5

    def _f(self, state):
        """State transition: gravitational propagation."""
        x, y, z, vx, vy, vz = state
        r = np.sqrt(x**2 + y**2 + z**2)
        if r < 1e-6:
            r = 1e-6
        ax = -MU * x / r**3
        ay = -MU * y / r**3
        az = -MU * z / r**3
        dt = self.dt
        return np.array([
            x + vx * dt + 0.5 * ax * dt**2,
            y + vy * dt + 0.5 * ay * dt**2,
            z + vz * dt + 0.5 * az * dt**2,
            vx + ax * dt,
            vy + ay * dt,
            vz + az * dt,
        ])

    def _get_jacobian_f(self):
        """Linearized state transition matrix F."""
        dt = self.dt
        F = np.eye(self.n)
        F[:3, 3:6] = np.eye(3) * dt
        return F

    def predict(self):
        """EKF prediction step."""
        F = self._get_jacobian_f()
        self.state = self._f(self.state)
        self.P = F @ self.P @ F.T + self.Q

    def update(self, z):
        """EKF update step. z can be 3D (position) or full state (6D)."""
        z = np.asarray(z, dtype=float)
        m = len(z)  # measurement dimension

        # Build H and R dynamically based on measurement size
        H = np.eye(m, self.n)  # observes first m components
        R = np.eye(m) * 0.5

        y = z - H @ self.state
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.state = self.state + K @ y
        self.P = (np.eye(self.n) - K @ H) @ self.P
