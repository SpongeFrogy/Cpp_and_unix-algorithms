#include <iostream> //standart
#include <cmath> //for pow()
#include <time.h> //magure time
#include <stdlib.h> // random number from _start to _end
#include <stdio.h>
#include <string.h>

using namespace std;
//https://www.geeksforgeeks.org/command-line-arguments-in-c-cpp/
int main(int argc, char* argv[])
{
    string opr = argv[2];
    if (opr == "plus")
    {
        double x1 = std::stod(argv[1]);
        double x2 = std::stod(argv[3]);
        cout<<x1+x2;
        return 0;
    }
    if (opr == "minus")
    {
        double x1 = std::stod(argv[1]);
        double x2 = std::stod(argv[3]);
        std::cout<<x1-x2;
        return 0;
    }
    if (opr == "power")
    {
        double x1 = std::stod(argv[1]);
        double x2 = std::stod(argv[3]);
        std::cout<<pow(x1, x2);
        return 0;
    }
    return 0;
}