import streamlit as st
import plotly.graph_objects as go
import networkx as nx

# --- App başlığı ---
st.set_page_config(page_title="Neyron Şəbəkə Animasiya", layout="wide")
st.title("🧠 Neyron Şəbəkə Axın Animasiya (Gözəl Görünüş + Web)")

# --- Qraf qur ---
G = nx.DiGraph()
input_nodes, hidden1_nodes, hidden2_nodes = 4, 5, 5
pos = {}

for i in range(input_nodes):
    pos[f"input_{i}"] = (-1, i - input_nodes / 2)
for i in range(hidden1_nodes):
    pos[f"h1_{i}"] = (0, i - hidden1_nodes / 2)
for i in range(hidden2_nodes):
    pos[f"h2_{i}"] = (1, i - hidden2_nodes / 2)
pos["output"] = (2, 0)

for i in range(input_nodes):
    for j in range(hidden1_nodes):
        G.add_edge(f"input_{i}", f"h1_{j}")
for i in range(hidden1_nodes):
    for j in range(hidden2_nodes):
        G.add_edge(f"h1_{i}", f"h2_{j}")
for i in range(hidden2_nodes):
    G.add_edge(f"h2_{i}", "output")

# Kənar və node koordinatları
edge_x, edge_y = [], []
for u, v in G.edges():
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

node_x = [pos[n][0] for n in G.nodes()]
node_y = [pos[n][1] for n in G.nodes()]
node_labels = [n.replace("_", " ").title() for n in G.nodes()]

# --- Başlanğıc boş signal trace (vacibdir) ---
signal_trace = go.Scatter(
    x=[], y=[], mode="markers",
    marker=dict(size=16, color=[]), hoverinfo="none"
)

# --- Axış yolları və animasiya frame-ləri ---
paths = [
    ["input_0", "h1_0", "h2_0", "output"],
    ["input_1", "h1_2", "h2_3", "output"],
    ["input_3", "h1_4", "h2_1", "output"]
]
colors = ['red', 'blue', 'green']

frames = []
for f in range(30):
    sig_x, sig_y, sig_c = [], [], []
    for path, c in zip(paths, colors):
        idx = (f // 10) % (len(path) - 1)
        t = (f % 10) / 10
        sx, sy = pos[path[idx]]
        tx, ty = pos[path[idx + 1]]
        x = sx * (1 - t) + tx * t
        y = sy * (1 - t) + ty * t
        sig_x.append(x); sig_y.append(y); sig_c.append(c)
    frames.append(go.Frame(data=[
        go.Scatter(x=edge_x, y=edge_y, mode='lines',
                   line=dict(color='lightblue', width=1), hoverinfo='none'),
        go.Scatter(x=node_x, y=node_y, mode='markers+text',
                   marker=dict(size=30, color='skyblue'),
                   text=node_labels, textposition="middle center"),
        go.Scatter(x=sig_x, y=sig_y, mode="markers",
                   marker=dict(size=16, color=sig_c), hoverinfo="none")
    ]))

# --- Başlanğıc figür ---
fig = go.Figure(
    data=[
        go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(color='lightblue', width=1), hoverinfo='none'),
        go.Scatter(x=node_x, y=node_y, mode='markers+text',
                   marker=dict(size=30, color='skyblue'),
                   text=node_labels, textposition="middle center"),
        signal_trace
    ],
    layout=go.Layout(
        title="Neyron Şəbəkədə Siqnal Axını",
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=50, b=20),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="▶ Play", method="animate",
                          args=[None, {"frame": {"duration": 200}, "fromcurrent": True}])],
            x=0.05, y=1.15
        )]
    ),
    frames=frames
)

# --- Streamlit-də göstər ---
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
✅ Drag və zoom et.  
✅ Girişdən çıxışa animasiyalı siqnal axını.  
✅ PyVis kimi görünüş + Plotly kimi hərəkət 👌
""")
