#include "thread_lib.h"
#include <iostream>
#include <chrono>

ThreadManager::ThreadManager(int max_threads)
    : max_threads(std::min(max_threads, (int)std::thread::hardware_concurrency())), sem(max_threads) {}

ThreadManager::~ThreadManager() {
    waitForCompletion();
}

void ThreadManager::executeTask(std::function<void()> task) {
    sem.acquire();  // Wait if max threads are in use

    std::lock_guard<std::mutex> lock(mtx);
    workers.emplace_back(&ThreadManager::threadWorker, this, task);
}

void ThreadManager::threadWorker(std::function<void()> task) {
    task();
    sem.release();  // Free a slot
}

void ThreadManager::waitForCompletion() {
    for (std::thread &t : workers) {
        if (t.joinable()) t.join();
    }
}

// Simulated workloads
double single_thread_workload() {
    auto start = std::chrono::high_resolution_clock::now();
    std::this_thread::sleep_for(std::chrono::milliseconds(50));  // Simulating work
    auto end = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double>(end - start).count();
}

double multi_thread_workload() {
    int thread_count = std::thread::hardware_concurrency();  // Use max available cores
    ThreadManager manager(thread_count);
    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < thread_count; i++) {  // Spawn only as many threads as cores
        manager.executeTask([]() {
            std::this_thread::sleep_for(std::chrono::milliseconds(20));  // Simulate work
        });
    }

    manager.waitForCompletion();
    auto end = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double>(end - start).count();
}
