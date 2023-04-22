#include <iostream> //standart
#include <cmath> //for pow()
#include <time.h> //magure time
#include <stdlib.h> // random number from _start to _end
#include <thread>
#include <chrono>
// https://stackoverflow.com/questions/2808398/easily-measure-elapsed-time
// for seeing time 
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
int n = 100000;

double sec1 = time1(1, n);
cout<< sec1 <<"s., N="<<n<<"\t"<<"без задержки"<<endl;

n = 1000;
double sec2 = time1_s(1, n);
cout<< sec2 <<"s., N="<<n<<"\t"<<"с задержкой: 0.01s."<<endl;

return 0;
}