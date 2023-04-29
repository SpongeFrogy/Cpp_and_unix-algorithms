#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <cmath> //for pow()
#include <time.h> //magure time

int main() {
    double x = 2;
    int n = 10000;
    double buf[n];

    clock_t start = clock();

    int pipe1[2], pipe2[2];
    if (pipe(pipe1) == -1 || pipe(pipe2) == -1) {
        std::cerr << "Failed to create pipes." << std::endl;
        return 1;
    }
    pid_t pid1 = fork();
    if (pid1 == -1) {
        std::cerr << "Failed to fork first child process." << std::endl;
        return 1;
    } else if (pid1 == 0) {
        // First child process
        
        double result1[n];
        for (int i = 0; i < n; i++) {
            close(pipe1[0]); // Close read end of pipe 1
            close(pipe2[0]); // Close read end of pipe 2
            close(pipe2[1]); // Close write end of pipe 2
            result1[i] = pow(x, 2) - pow(x, 2) + pow(x, 4) - pow(x, 5) + x + x;
            write(pipe1[1], result1, sizeof(result1)); // Write result to pipe 1
            close(pipe1[1]); // Close write end of pipe 1
        }
        return 0;
    }
    pid_t pid2 = fork();
    if (pid2 == -1) {
        std::cerr << "Failed to fork second child process." << std::endl;
        return 1;
    } else if (pid2 == 0) {
        // Second child process
        double result2[n];
        for (int i = 0; i < n; i++) {
            close(pipe2[0]); // Close read end of pipe 2
            close(pipe1[0]); // Close read end of pipe 1
            close(pipe2[1]); // Close write end of pipe 2
            result2[i] = pow(x, 2) - pow(x, 2) + pow(x, 4) - pow(x, 5) + x + x;
            write(pipe2[1], result2, sizeof(result2)); // Write result to pipe 2
            close(pipe2[1]); // Close write end of pipe 2

        }
        return 0;
    }
    // Parent process
    close(pipe1[0]); // Close read end of pipe 1
    close(pipe1[1]); // Close write end of pipe 1
    close(pipe2[1]); // Close write end of pipe 2
    double  allRes;
    double result2[n];
    read(pipe2[0], result2, sizeof(result2)); // Read result from pipe 2
    double result1[n];
    read(pipe1[0], result1, sizeof(result1)); // Read result from pipe 1
    for (int i = 0; i < n; i++) {
        allRes = result1[i] + result2[i] - result1[i];
    }
    // Wait for child processes to exit
    int status;
    waitpid(pid1, &status, 0);
    waitpid(pid2, &status, 0);

    clock_t end = clock();
    double seconds = (double)(end - start) / CLOCKS_PER_SEC;
    std:: cout << "for n="<<n<< " with processes time is: " << seconds << " s.";

    return 0;
}