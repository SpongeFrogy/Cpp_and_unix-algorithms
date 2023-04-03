#include <iostream> //standart
#include <cmath> //for pow()
#include <time.h> //magure time
#include <stdlib.h> // random number from _start to _end

using namespace std;

// int [−2 147 483 648:2 147 483 647] 4 bytes
// long 8 bytes

double func(const int &x, const int &n)
{
    clock_t start = clock(); // time of start in flops
    for(int i; i < n; i++) // new i; i=0,1,...,n; i = i+1
    {
        float res = pow(x, 2) - pow(x, 2) + x * 4 - x * 5 + x + x; //float result
    }
    clock_t end = clock(); // time of end in flops
    double seconds = (double)(end - start) / CLOCKS_PER_SEC; // megured time in flobs / flops per second
    std::cout << seconds << endl;
    printf("The time: %.5e seconds\n", seconds); // print  megured time in seconds
    return seconds; //return megured time in seconds
}

int main()
{
    string answer = "y"; //set answer
    while (answer == "y") // while loop, if snaswer != 'n', then breack
    {
        float x = rand() % 2+100; // random number
        // ask for input
        int n; 
        std::cout << "Enter the number of loops:" << endl;
        std::cin >> n;
        // is the input acceptable
        if(!std::cin.good()) // !std::cin.good('y') = False
        {
            std::cout << "Thats not int" << endl;
            return 0; // break
        }
        std::cout << "Thats int" << endl; // all good
        double res =  func(x, n);
        std::cout << "Again [y/n]?" << endl; // ask for another loop
        std::cin >> answer;
    }
}
