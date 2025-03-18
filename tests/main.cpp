#include <iostream>
#include <fstream>
#include <filesystem>
#include "../include/thread_lib.h" // Include thread library header

int main() {
    // Measure execution times
    double single_time = single_thread_workload();
    double multi_time = multi_thread_workload();

    // Display execution times
    std::cout << "Single Thread Execution Time: " << single_time << " seconds\n";
    std::cout << "Multi-Threaded Execution Time: " << multi_time << " seconds\n";

    // Define the absolute path to execution_times.txt in the project root
    std::string filePath = "/home/tejdeepak/ThreadLibrary/execution_times.txt";


    // Write execution times to file
    std::ofstream outFile(filePath, std::ios::trunc);
    if (outFile.is_open()) {
        outFile << single_time << " " << multi_time << std::endl;
        outFile.flush(); // Ensure data is written
        outFile.close(); // Close the file
        std::cout << "✅ Updated execution_times.txt successfully at: " << filePath << "\n";
    } else {
        std::cerr << "❌ Failed to open execution_times.txt for writing!\n";
    }

    return 0;
}
