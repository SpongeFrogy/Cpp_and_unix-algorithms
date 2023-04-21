#include <iostream> //standart
#include <cmath> //for pow()
#include <time.h> //magure time
#include <stdlib.h> // random number from _start to _end
#include <thread>
#include <chrono>

using namespace std;

// return time in microseconds
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


int main()
{
double x = 1;
int n = 1000;
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

n = 100;
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