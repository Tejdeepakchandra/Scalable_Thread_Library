#ifndef THREAD_LIB_H
#define THREAD_LIB_H

#include <vector>
#include <thread>
#include <mutex>
#include <semaphore>
#include <functional>

class ThreadManager {
public:
    ThreadManager(int max_threads);
    ~ThreadManager();

    void executeTask(std::function<void()> task);
    void waitForCompletion();

private:
    int max_threads;
    std::vector<std::thread> workers;
    std::mutex mtx;
    std::counting_semaphore<1000> sem; // Fix: Replace std::binary_semaphore (C++20-only) with counting_semaphore

    void threadWorker(std::function<void()> task);
};

// Workload simulation functions
double single_thread_workload();
double multi_thread_workload();

#endif