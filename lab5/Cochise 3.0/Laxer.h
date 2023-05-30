#include "Token.h"

class Laxer
{
    public:
    string Code;
    int pos = 0;
    vector<Token> tokenList;

    Laxer(string code): Code(code)
    {}

    vector<Token> lexAnalysis();
    bool nextToken();

};