## Project Overview
The Scalable Thread Management Library enables developers to execute tasks in parallel using a thread pool, optimizing performance on multi-core systems. It provides a simple API for task submission, ensures thread safety with mutexes and condition variables, and measures performance through a computationally intensive workload (sum of squares).

**Key Goals**:
- Build a reusable thread pool for parallel processing.
- Ensure thread-safe task submission and execution.
- Achieve significant speedup (e.g., ~3x on 8-core CPU).
- Save execution times for analysis.

## Features
- **Thread Pool Management**: Creates a pool of worker threads (capped at CPU cores) to minimize overhead.
- **Task Submission**: Supports flexible task submission via `std::function<void()>` (e.g., lambdas, functions).
- **Thread Safety**: Uses `std::mutex` and `std::condition_variable` to prevent race conditions and deadlocks.
- **Performance Testing**: Compares single-threaded vs. multi-threaded execution for a sum-of-squares workload.
- **Output Storage**: Saves execution times to `execution_times.txt` for analysis.
- **Error Handling**: Robust handling of file operations and task execution exceptions.

## System Architecture
The library is modular, with three core components interacting as shown below:

```mermaid
graph TD
    A[User] -->|Submits Tasks| B[ThreadManager]
    B -->|Manages| C[Task Queue]
    C -->|Distributes Tasks| D[Worker Threads]
    D -->|Executes Tasks| E[Results]
    E -->|Saves| F[Output File: execution_times.txt]
