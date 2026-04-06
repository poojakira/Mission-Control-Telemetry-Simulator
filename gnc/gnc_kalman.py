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
        # Measurement matrix (measure position only, first 3 states)
        self.H = np.zeros((3, self.n))
        self.H[:3, :3] = np.eye(3)
        # Measurement noise
        self.R = np.eye(3) * 0.5

    def _f(self, state):
        """State transition: simple linear ballistic propagation."""
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

    def _get_jacobian_f(self, state):
        """Linearized state transition matrix F."""
        dt = self.dt
        F = np.eye(self.n)
        F[:3, 3:6] = np.eye(3) * dt
        return F

    def predict(self):
        """EKF prediction step."""
        F = self._get_jacobian_f(self.state)
        self.state = self._f(self.state)
        self.P = F @ self.P @ F.T + self.Q

    def update(self, z):
        """EKF update step with measurement z (position, shape (3,))."""
        z = np.asarray(z)
        y = z - self.H @ self.state
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.state = self.state + K @ y
        self.P = (np.eye(self.n) - K @ self.H) @ self.P
