import numpy as np
import plotly.graph_objs as go

def attractor(data, arr = [0,1,2], msg="Takens Embedding"):
    print(f"Window shape:   {data.shape}")

    if data.shape[1]>2:
        x,y,z = data[:, arr[0]], data[:, arr[1]], data[:, arr[2]]
    else:
        x,y,z = data[:, 0], data[:, 1], np.zeros(len(data), )

    print("Unique x:", len(np.unique(x)))
    print("Unique y:", len(np.unique(y)))
    print("Unique z:", len(np.unique(z)))

    fig = go.Figure(data=[go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(
                size=5,
                color=x,                # Set color to vary by Y value
                colorscale='Viridis',   # Choose a colorscale
                opacity=0.8
            )
        )])

    fig.update_layout(
        title=msg,
        scene = dict(aspectmode = 'manual')
    )

    fig.show()

