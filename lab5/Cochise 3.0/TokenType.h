#include <iostream>
#include <map>
#include <vector>
#include <regex>

using namespace std;

class TokenType
{   public:
    string Name;
    regex  Regex;
    TokenType(string name, regex regex): Name(name), Regex(regex)
    {}

};

