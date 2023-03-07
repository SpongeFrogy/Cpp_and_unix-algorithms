#include <iostream>
#include <cmath>
using namespace std;

int func(const float &x)
{
    return x*x-x*x+x*4-x*5+x+x;
}
// main() is where program execution begins.
int main() {
   cout << func(5);
   return 0;
}
