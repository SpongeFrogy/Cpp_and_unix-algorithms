#include "TokenType.h"

class Token
{
    public:
    TokenType Type;
    string Text;
    int Pos;
    Token(TokenType type, string text, int pos): Type(type), Text(text), Pos(pos)
    {}
};
