import matplotlib.pyplot as plt
import networkx as nx
import os

def generate_intelligence_graph(records):
    G = nx.Graph()

    phone = None
    locations = set()
    crimes = set()

    for r in records:
        if r.get("phone"):
            phone = r["phone"]
        if r.get("state"):
            locations.add(r["state"])
        if r.get("crime"):
            crimes.add(r["crime"])

    if not phone:
        return None

    # Add central phone node
    G.add_node(phone, type="phone")

    # Add locations
    for loc in locations:
        G.add_node(loc, type="location")
        G.add_edge(phone, loc)

    # Add crimes
    for crime in crimes:
        G.add_node(crime, type="crime")
        G.add_edge(phone, crime)

    # -------- FIXED POSITIONS (VERY CLEAN) --------
    pos = {phone: (0, 0)}

    y_offset = 2
    for i, crime in enumerate(crimes):
        pos[crime] = (0, y_offset + i*1.5)

    x_offset = 3
    for i, loc in enumerate(locations):
        pos[loc] = ((-1)**i * x_offset, -1.5)

    # -------- COLORS --------
    colors = []
    sizes = []

    for node in G.nodes():
        t = G.nodes[node]["type"]
        if t == "phone":
            colors.append("#e74c3c")   # red
            sizes.append(3200)
        elif t == "location":
            colors.append("#3498db")   # blue
            sizes.append(2200)
        else:
            colors.append("#f39c12")   # orange
            sizes.append(2200)

    plt.figure(figsize=(8, 6))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=sizes,
        font_size=11,
        font_weight="bold",
        edge_color="#333333",
        width=2
    )

    plt.title("Crime Intelligence Summary Graph", fontsize=14, fontweight="bold")
    plt.axis("off")

    path = os.path.join("uploads", "intelligence_graph.png")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return path
