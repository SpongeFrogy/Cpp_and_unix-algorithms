#include <iostream> //standart
#include <cmath> //for pow()
#include <time.h> //magure time
#include <stdlib.h> // random number from _start to _end
#include <stdio.h>
#include <string.h>

using namespace std;
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

int main()
{
    std::string s;
    std::cout<<"example:1.23plus4.46\ncommands:plus / minus / power\n";
    std::cout<<"Write a command:";
    std::cin>>s;
    //size_t pos = s.find("plus");
    if (s.find("plus") != std::string::npos)
    {
        size_t pos = s.find("plus");
        double x1 = std::stod(s.substr(0, pos));
        double x2 = std::stod(s.substr(pos+4));
        std::cout<<"="<<x1+x2;
        return 0;
    }
    if (s.find("minus") != std::string::npos)
    {
        size_t pos = s.find("minus");
        double x1 = std::stod(s.substr(0, pos));
        double x2 = std::stod(s.substr(pos+5));
        std::cout<<"="<<x1-x2;
        return 0;
    }
    if (s.find("power") != std::string::npos)
    {
        size_t pos = s.find("power");
        double x1 = std::stod(s.substr(0, pos));
        double x2 = std::stod(s.substr(pos+5));
        std::cout<<"="<<pow(x1, x2);
=======
=======
>>>>>>> main
=======
>>>>>>> main
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
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> main
=======
>>>>>>> main
=======
>>>>>>> main
        return 0;
    }
    return 0;
}