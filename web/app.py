import os
import time
from flask import Flask, render_template, request
import matplotlib.pyplot as plt

app = Flask(__name__)

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # ~/testinglib/web/
FILE_PATH = os.path.join(BASE_DIR, "..", "execution_times.txt")  # ~/testinglib/execution_times.txt
GRAPH_PATH = os.path.join(BASE_DIR, "static", "execution_graph.png")  # ~/testinglib/web/static/execution_graph.png
BENCHMARK_PATH = os.path.join(BASE_DIR, "..", "thread_benchmark")  # ~/testinglib/thread_benchmark

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
        else:
            print(f"❌ File not found: {FILE_PATH}")
    except Exception as e:
        print(f"❌ Error reading {FILE_PATH}: {e}")

    return round(single_thread_time, 6), round(thread_pool_time, 6)

def generate_graph(single_thread_time, thread_pool_time):
    try:
        labels = ["Single Thread", "Thread Pool"]
        times = [single_thread_time, thread_pool_time]

        plt.figure(figsize=(6, 4))
        plt.bar(labels, times, color=["#3498db", "#2ecc71"])
        plt.xlabel("Execution Type")
        plt.ylabel("Time (seconds)")
        plt.title("Thread Performance Comparison")
        plt.tight_layout()
        plt.savefig(GRAPH_PATH)
        plt.close()
        print(f"✅ Graph saved to {GRAPH_PATH}")
    except Exception as e:
        print(f"❌ Failed to generate graph: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    single_thread_time, thread_pool_time = read_execution_times()
    graph_available = os.path.exists(GRAPH_PATH)

    if request.method == "POST":
        print("🔄 Running thread_benchmark...")
        result = os.system(BENCHMARK_PATH)
        
        if result == 0:
            time.sleep(1)
            single_thread_time, thread_pool_time = read_execution_times()
            generate_graph(single_thread_time, thread_pool_time)
            graph_available = True
        else:
            print("❌ Benchmark failed to run—check if thread_benchmark exists and is executable.")

    graph_rel_path = "static/execution_graph.png" if graph_available else None
    
    return render_template("index.html", 
                          single_thread_time=single_thread_time,
                          thread_pool_time=thread_pool_time,
                          graph_path=graph_rel_path)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)