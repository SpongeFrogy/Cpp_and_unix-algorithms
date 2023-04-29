
# ЛР #4: [C++ & UNIX]: C++ PROCESSES / THREADS

Карсаков Григорий Вячеславович, 3 курс (ФизФ ИТМО), Z33434, 2023

## Цель

Познакомить студента с принципами параллельных вычислений. Составить несколько
программ в простейшими вычислительными действиями, чтобы освоить принципы
параллельных вычислений (когда одни алгоритмы зависят / не зависят от других).

## Решение

1. [С++ SEQUENCE] Последовательные вычисления

Требуется последовательно выполнить вычисления по формуле 1, вычисления по
формуле 2, после чего выполнить вычисления по формуле 3, которые выглядят
следующим образом: результат вычислений 1 + результат вычислений 2 –
результат вычислений 1
Выполнить последовательно на 10 000 итераций и 100 000 итераций:

- Формула 1: `f(x) = x ^2- x ^2+ x *4- x *5+ x + x`
- Формула 2: `f(x) = x + x`

Вывести длительность выполнения всех 10 000 итераций и 100 000 итераций в сек.

```C++
double func1(const double &x)
{
double y = pow(x, 2) - pow(x, 2) + pow(x, 4) - pow(x, 5) + x + x;
return y;
}


// 
double func2(const double &x)
{
double y = x + x;
return y;
}

double func3(const double &res1, const double &res2)
{
double y = res1 + res2 - res1;
return y;
}



double time1_s(const double &x, const int &n)
{
clock_t start = clock();
for(int i; i < n; i++)
{
    double res1 = func1(x);
    this_thread::sleep_for(chrono::milliseconds(10));
    double res2 = func2(x);
    this_thread::sleep_for(chrono::milliseconds(10));
    double res3 = func3(res1, res2);
}
clock_t end = clock(); // time of end in flops
double seconds = (double)(end - start) / CLOCKS_PER_SEC;
return seconds;
}

double time1(const double &x, const int &n)
{
clock_t start = clock();
for(int i; i < n; i++)
{
    double res1 = func1(x);
    double res2 = func2(x);
    double res3 = func3(res1, res2);
}
clock_t end = clock(); // time of end in flops
double seconds = (double)(end - start) / CLOCKS_PER_SEC;
return seconds;
}

int main()
{
double x = 1;
int n = 1000;

double sec1 = time1(1, n);
cout<< sec1 <<"s., N="<<n<<"\t"<<"без задержки"<<endl;

n = 100;
double sec2 = time1_s(1, n);
cout<< sec2 <<"s., N="<<n<<"\t"<<"с задержкой: 0.01s."<<endl;

return 0;
}
```

2. [C++ THREADS] Параллельные вычисления через потоки

Требуется параллельно (насколько возможно с помощью потоков) выполнить
вычисления по формуле 1, вычисления по формуле 2, после чего выполнить
вычисления по формуле 3, которые выглядят следующим образом: результат
вычислений 1 + результат вычислений 2 – результат вычислений 1
Выполнить последовательно на 10 000 итераций и 100 000 итераций

- Формула 1: `f(x) = x ^2- x ^2+ x *4- x*5+ x + x`
- Формула 2: `f(x) = x + x`

Вывести длительность выполнения всех 10 000 итераций и 100 000 итераций в сек.
в разбивке по шагам вычислений 1, 2 и 3

```C++
int main()
{
double x = 1;
int n = 100000;
clock_t start = clock();
for(int i; i < n; i++)
{
    double res1;
    double res2;
    thread th1([&res1, &x]()
    {
        res1 = func1(x);
    });
    thread th2([&res2, &x]()
    {
        res2 = func2(x);
    });
    th1.join();
    th2.join();
    double res3 = func3(res1, res2); 
}
clock_t end = clock(); // time of end in flops
double seconds = (double)(end - start) / CLOCKS_PER_SEC;
cout<< seconds<<"s., N="<<n<<"\t"<<"без задержки"<<endl;

n = 1000;
start = clock();
for(int i; i < n; i++)
{
    double res1;
    double res2;
    thread th1([&res1, &x]()
    {
        res1 = func1(x);
        this_thread::sleep_for(chrono::milliseconds(10));
    });
    thread th2([&res2, &x]()
    {
        res2 = func2(x);
        this_thread::sleep_for(chrono::milliseconds(10));
    });
    th1.join();
    th2.join();
    double res3 = func3(res1, res2); 
}
end = clock(); // time of end in flops
seconds = (double)(end - start) / CLOCKS_PER_SEC;
cout<< seconds<<"s., N="<<n<<"\t"<<"с задержкой:0.01s."<<endl;

return 0;
}
```

Теперь приведем пример другой реализации:

```C++
#include <iostream> //standart
#include <cmath> //for pow()
#include <time.h> //magure time
#include <stdlib.h> // random number from _start to _end
#include <thread>
#include <chrono>
#include <mutex>
#include <queue>

using namespace std;


int main()
{
double x = 1;
int n = 10000;
double res1[n];
double res2[n];
std::mutex m;
clock_t start = clock();


thread th1([&res1, &x, &n, &m]()
{   
    for(int i = 0; i<n; i++)
    {
        double y = pow(x, 2) - pow(x, 2) + pow(x, 4) - pow(x, 5) + x + x;
        m.lock();
        res1[i] = y;
        m.unlock();
    }
});

thread th([&res2, &x, &n, &m]()
{   
    for(int i = 0; i < n; i++)
    {
        double y = x + x;
        m.lock();
        res2[i] = y;
        m.unlock();
    }
});

double res3; 

for(int i = 0; i<n; i++)
{
    res3 = res1[i] + res2[i] - res1[i];
    // std::cout << i << ',' << res3 << std::endl;
}
th1.join();
th.join();
clock_t end = clock(); // time of end in flops
double seconds = (double)(end - start) / CLOCKS_PER_SEC;
// std::cout<< seconds<<"s., N="<<n<<std::endl;
printf("For N = %i the elapsed time is %.5e seconds\n", n, seconds);
return 0;
}
```

3. [C++ PROCESS] Параллельные вычисления через процессы

Требуется параллельно (насколько возможно с помощью процессов) выполнить
вычисления по формуле 1, вычисления по формуле 2, после чего выполнить
вычисления по формуле 3, которые выглядят следующим образом: результат
вычислений 1 + результат вычислений 2 – результат вычислений 1
Выполнить последовательно на 10 000 итераций и 100 000 итераций
Формула 1: f(x) = x ^2- x ^2+ x *4- x*5+ x + x
Формула 2: f(x) = x + x
Вывести длительность выполнения всех 10 000 итераций и 100 000 итераций в сек.
в разбивке по шагам вычислений 1, 2 и 3

```C++
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
```

## Вывод

Результаты без задержки:
|**N**    |**straight time, s.**|**threads time, s.**|**processes time, s.**|
|---------|---------------------|--------------------|----------------------|
| 10 000  | 0.001              | 1.54/0.002         |  0.00033             |
| 100 000 | 0.003               | 15.823/0.02        |  0.001412            |

Результаты с задержкой 0.01 с.
|**N**    |**straight time, s.**|**threads time, s.**|**processes time, s.**|
|---------|---------------------|--------------------|----------------------|
| 100     | 3.182               | 0.674              | none                 |
| 1 000   | 32.142              | 15.087             | none                 |
