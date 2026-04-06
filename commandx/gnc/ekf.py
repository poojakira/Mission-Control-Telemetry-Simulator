import numpy as np

# WGS84 Constants (duplicated from mission_engine for autonomy)
MU = 398600.4418
R_EARTH = 6378.137
J2 = 1.08262668e-3

class ExtendedKalmanFilter:
    """
    Estimates true state [x, y, z, vx, vy, vz] from noisy measurements
    using non-linear orbital dynamics (Universal Gravitation + J2).
    """
    def __init__(self, initial_state, dt):
        self.state = initial_state.copy()
        self.dt = dt

        # Covariance Matrix (Initial Uncertainty)
        self.P = np.eye(6) * 1.0

        # Process Noise (Physics isn't perfect)
        self.Q = np.eye(6) * 0.0001

        # Measurement Matrix (We measure all 6 states)
        self.H = np.eye(6)

        # Measurement Noise (Sensor Specs)
        self.R = np.eye(6) * 0.5

    def _get_jacobian_f(self, state):
        """Calculates the Jacobian of the state transition function."""
        r_vec = state[:3]
        r_mag = np.linalg.norm(r_vec)
        r_mag_sq = r_mag**2

        # 1. Gravity Gradient Matrix (G)
        # G = -mu/r^3 * (I - 3rr^T/r^2)
        I = np.eye(3)
        outer_p = np.outer(r_vec, r_vec)
        G = -(MU / (r_mag**3)) * (I - (3.0 * outer_p / r_mag_sq))

        # 2. Assemble 6x6 F matrix
        # F = [ 0 I ]
        #     [ G 0 ]
        F = np.zeros((6, 6))
        F[:3, 3:] = I
        F[3:, :3] = G

        # Discrete transition matrix (first-order Euler)
        return np.eye(6) + F * self.dt

    def predict(self, accel_command=None):
        """Propagate state and covariance using non-linear dynamics."""
        # FIX: avoid mutable default argument — use None sentinel instead
        if accel_command is None:
            accel_command = np.zeros(3)

        r_vec = self.state[:3]
        r_mag = np.linalg.norm(r_vec)

        # 1. State Extrapolation (Newton's Laws + Gravity)
        gravity_accel = -(MU / (r_mag**3)) * r_vec

        # J2 Perturbation
        k = (1.5 * J2 * MU * (R_EARTH**2)) / (r_mag**5)
        j2_accel = np.array([
            k * r_vec[0] * (5 * r_vec[2]**2 / r_mag**2 - 1),
            k * r_vec[1] * (5 * r_vec[2]**2 / r_mag**2 - 1),
            k * r_vec[2] * (5 * r_vec[2]**2 / r_mag**2 - 3)
        ])
        total_accel = gravity_accel + j2_accel + accel_command

        # FIX: Compute Jacobian BEFORE updating state so it linearises
        # at the current operating point, not the future predicted one.
        Phi = self._get_jacobian_f(self.state)

        # Euler Integration
        self.state[:3] += self.state[3:] * self.dt + 0.5 * total_accel * self.dt**2
        self.state[3:] += total_accel * self.dt

        # Covariance Extrapolation: P = FPF' + Q
        self.P = Phi @ self.P @ Phi.T + self.Q

    def update(self, measurement):
        """Update state using linear/linearized measurement model."""
        # 1. Calculate Kalman Gain: K = PH' (HPH' + R)^-1
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)

        # 2. Update State Estimate: x = x + K(y - Hx)
        innovation = measurement - (self.H @ self.state)
        self.state = self.state + (K @ innovation)

        # 3. Update Uncertainty: P = (I - KH)P
        I = np.eye(6)
        self.P = (I - K @ self.H) @ self.P
        return self.state
