import plotly.graph_objects as go
import numpy as np

class TacticalDisplay:
    """
    Renders 3D Orbital Trajectories and Sensor Cones.
    """
    @staticmethod
    def create_3d_plot(history_data):
        # FIX: guard against empty history_data to prevent IndexError on x[0]/y[0]/z[0]
        if not history_data:
            return go.Figure()

        # Unpack History
        x = [s[0] for s in history_data]
        y = [s[1] for s in history_data]
        z = [s[2] for s in history_data]

        fig = go.Figure()

        # 1. The Flight Path
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color=list(range(len(x))), colorscale='Plasma', width=6),
            name='Trajectory'
        ))

        # 2. The Target (Docking Port)
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(size=12, color='#00ff00', symbol='diamond'),
            name='Target Port'
        ))

        # 3. Start Point
        fig.add_trace(go.Scatter3d(
            x=[x[0]], y=[y[0]], z=[z[0]],
            mode='markers',
            marker=dict(size=8, color='#ff0000'),
            name='Injection'
        ))

        # 4. Approach Cone (Visual Guide)
        cone_length = 200
        cone_radius = cone_length * np.tan(np.radians(15))

        fig.add_trace(go.Scatter3d(
            x=[0, -cone_length, -cone_length, -cone_length, -cone_length, 0],
            y=[0, cone_radius, -cone_radius, 0, 0, 0],
            z=[0, 0, 0, cone_radius, -cone_radius, 0],
            mode='lines',
            line=dict(color='rgba(255,255,0,0.3)', width=2),
            name='Approach Cone'
        ))

        fig.update_layout(
            scene=dict(
                xaxis_title='X (km)',
                yaxis_title='Y (km)',
                zaxis_title='Z (km)',
                bgcolor='rgba(0,0,0,0)',
                xaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.1)'),
                zaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.1)'),
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc'),
            legend=dict(bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=30, b=0),
            height=500
        )
        return fig
