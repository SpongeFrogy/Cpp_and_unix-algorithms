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
int n = 100000;
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