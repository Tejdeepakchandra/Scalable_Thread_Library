import os
import time
from flask import Flask, render_template, request
import matplotlib.pyplot as plt

app = Flask(__name__)

# File paths
FILE_PATH = "../execution_times.txt"  # Assuming it is in the same folder
GRAPH_PATH = "static/execution_graph.png"

def read_execution_times():
    single_thread_time = 0.0
    thread_pool_time = 0.0

    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as file:
                times = file.read().strip().split()
                if len(times) == 2:
                    single_thread_time = float(times[0])
                    thread_pool_time = float(times[1])
    except Exception as e:
        print("❌ Error reading execution_times.txt:", e)

    return round(single_thread_time, 6), round(thread_pool_time, 6)

def generate_graph(single_thread_time, thread_pool_time):
    labels = ["Single Thread", "Thread Pool"]
    times = [single_thread_time, thread_pool_time]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, times, color=["blue", "green"])
    plt.xlabel("Execution Type")
    plt.ylabel("Execution Time (s)")
    plt.title("Thread Execution Performance")
    plt.savefig(GRAPH_PATH)
    plt.close()

@app.route("/", methods=["GET", "POST"])
def index():
    single_thread_time, thread_pool_time = read_execution_times()
    graph_available = False  # Initially, no graph

    if request.method == "POST":
        print("🔄 Running thread_benchmark...")
        os.system("./thread_benchmark")  # Run benchmark from correct location

        # Wait for execution to complete
        time.sleep(1)

        single_thread_time, thread_pool_time = read_execution_times()
        generate_graph(single_thread_time, thread_pool_time)  # Generate graph
        graph_available = True  # Now the graph is available

    return render_template("index.html", 
                           single_thread_time=str(single_thread_time), 
                           thread_pool_time=str(thread_pool_time),
                           graph_path=GRAPH_PATH if graph_available else None)  # Only show graph if available

if __name__ == "__main__":
    app.run(debug=True)
