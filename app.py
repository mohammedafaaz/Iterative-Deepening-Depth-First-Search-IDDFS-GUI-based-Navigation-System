
import tkinter as tk
from tkinter import ttk
import tracemalloc

ballari_map = {
    "Ballari": [("Hospet",64),("Siruguppa",55),("Sandur",40),("Kurugodu",22),("Toranagallu",22)],
    "Hospet": [("Ballari",64),("Kampli",33),("Sandur",27),("Kudligi",41),("Hagaribommanahalli",38)],
    "Sandur": [("Ballari",40),("Hospet",27),("Kudligi",29),("Toranagallu",17),("Hagaribommanahalli",35)],
    "Siruguppa": [("Ballari",55),("Kampli",50),("Kurugodu",35)],
    "Kampli": [("Hospet",33),("Siruguppa",50),("Ballari",45)],
    "Kudligi": [("Sandur",29),("Hospet",41),("Hagaribommanahalli",25),("Ballari",70)],
    "Kurugodu": [("Ballari",22),("Siruguppa",35)],
    "Hagaribommanahalli": [("Hospet",38),("Sandur",35),("Kudligi",25)],
    "Toranagallu": [("Ballari",22),("Sandur",17)]
}

city_positions = {
    "Ballari": (450, 250),
    "Hospet": (300, 180),
    "Sandur": (350, 320),
    "Siruguppa": (600, 180),
    "Kampli": (500, 100),
    "Kudligi": (220, 380),
    "Kurugodu": (550, 300),
    "Hagaribommanahalli": (120, 250),
    "Toranagallu": (430, 380)
}

def dls(graph, current, goal, depth, visited):
    if current == goal:
        return [current]
    if depth == 0:
        return None

    visited.add(current)

    for neighbor, _ in graph.get(current, []):
        if neighbor not in visited:
            path = dls(graph, neighbor, goal, depth - 1, visited)
            if path:
                return [current] + path

    visited.remove(current)
    return None

def iddfs(graph, start, target):
    if start == target:
        return [start]

    for depth in range(len(graph) + 1):
        path = dls(graph, start, target, depth, set())
        if path:
            return path

    return None

def total_distance(graph, path):
    return sum(
        dist
        for i in range(len(path) - 1)
        for neighbor, dist in graph[path[i]]
        if neighbor == path[i + 1]
    )

def measure_memory(func):
    tracemalloc.start()
    result = func()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak / 1024

def draw_map(route=None):
    canvas.delete("all")

    drawn = set()

    for city, neighbors in ballari_map.items():
        x1, y1 = city_positions[city]

        for neighbor, dist in neighbors:
            edge = tuple(sorted([city, neighbor]))

            if edge in drawn:
                continue

            drawn.add(edge)

            x2, y2 = city_positions[neighbor]

            color = "#666666"
            width = 2

            if route:
                for i in range(len(route) - 1):
                    if {route[i], route[i+1]} == {city, neighbor}:
                        color = "#10a37f"
                        width = 5

            canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

            canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=str(dist),
                fill="white",
                font=("Segoe UI", 8)
            )

    for city, (x, y) in city_positions.items():
        node_color = "#444444"

        if route and city in route:
            node_color = "#10a37f"

        canvas.create_oval(
            x - 15, y - 15,
            x + 15, y + 15,
            fill=node_color,
            outline="white"
        )

        canvas.create_text(
            x,
            y - 25,
            text=city,
            fill="white",
            font=("Segoe UI", 9)
        )

def find_route():
    start = start_city.get()
    target = goal_city.get()

    path, ram = measure_memory(
        lambda: iddfs(ballari_map, start, target)
    )

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)

    if not path:
        output_text.insert(tk.END, "No Route Found")
        output_text.config(state="disabled")
        return

    output_text.insert(tk.END, "Delivery Route Found\n\n")
    output_text.insert(tk.END, f"Start City: {start}\n")
    output_text.insert(tk.END, f"Destination: {target}\n\n")
    output_text.insert(tk.END, f"Route:\n{' -> '.join(path)}\n\n")
    output_text.insert(tk.END, f"Stops: {len(path)-1}\n")
    output_text.insert(tk.END, f"Total Distance: {total_distance(ballari_map, path)} km\n")
    output_text.insert(tk.END, f"Peak RAM Usage: {ram:.2f} KB")

    output_text.config(state="disabled")

    draw_map(path)

root = tk.Tk()
root.title("IDDFS Navigation Assistant")
root.geometry("1200x800")
root.configure(bg="#212121")

header = tk.Label(
    root,
    text="IDDFS Delivery Navigation Assistant",
    bg="#212121",
    fg="white",
    font=("Segoe UI", 22, "bold")
)
header.pack(pady=15)

top_frame = tk.Frame(root, bg="#2f2f2f")
top_frame.pack(fill="x", padx=20, pady=10)

cities = sorted(ballari_map.keys())

tk.Label(top_frame, text="Start City", bg="#2f2f2f", fg="white").grid(row=0, column=0, padx=10, pady=10)

start_city = ttk.Combobox(top_frame, values=cities, width=25)
start_city.grid(row=0, column=1, padx=10)
start_city.current(0)

tk.Label(top_frame, text="Destination City", bg="#2f2f2f", fg="white").grid(row=1, column=0, padx=10, pady=10)

goal_city = ttk.Combobox(top_frame, values=cities, width=25)
goal_city.grid(row=1, column=1, padx=10)
goal_city.current(1)

tk.Button(
    top_frame,
    text="Find Route",
    command=find_route,
    bg="#10a37f",
    fg="white",
    font=("Segoe UI", 10, "bold")
).grid(row=2, column=0, columnspan=2, pady=15)

output_text = tk.Text(
    root,
    height=8,
    bg="#2f2f2f",
    fg="white",
    insertbackground="white"
)
output_text.pack(fill="x", padx=20, pady=10)
output_text.insert("1.0", "Select cities and click Find Route.")
output_text.config(state="disabled")

canvas = tk.Canvas(root, bg="#212121", highlightthickness=0)
canvas.pack(fill="both", expand=True, padx=20, pady=10)

draw_map()

root.mainloop()
