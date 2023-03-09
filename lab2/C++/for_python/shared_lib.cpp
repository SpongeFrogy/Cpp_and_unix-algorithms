#include "shared_lib.h"

double func(double x, long n)
{
    clock_t start = clock();
    for(int i; i < n+1; i++)
    {
        double res = pow(x, 2) - pow(x, 2) + x * 4 - x * 5 + x + x;
    }
    clock_t end = clock();
    double seconds = (double)(end - start) / CLOCKS_PER_SEC;
    printf("The time: %f seconds\n", seconds);
    return seconds;
}