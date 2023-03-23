#include <iostream> //standart
#include <cmath> //for pow()
#include <time.h> //magure time
#include <stdlib.h> // random number from _start to _end
#include <stdio.h>
#include <string.h>


using namespace std;

int main()
{
    char input;
    std::cout << "Write an operation:";
    std::cin >> input;
    std::string operand[4] = 
    {"calc", "plus", "minus", "power"};
    for(int i = 0; i<4; i++)
    {
        char *token = strtok(input, operand[i]);
   
        // Keep printing tokens while one of the
        // delimiters present in str[].
        while (token != NULL)
    {
        printf("%s\n", token);
        token = strtok(NULL, "-");
    }
    }
}