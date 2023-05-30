#include "Nodes.h"
#include <vector>

class Parser 
{
    public:
    vector<Token> tokens;
    int pos = 0;
    map<string, int> scope;

    Parser(vector<Token> tks): tokens(tks) {}

    Token match(vector<TokenType> expected);
    Token require(vector<TokenType> expected);

    ExpressionNode* parseCode();

    ExpressionNode* parseExpression();

    ExpressionNode* parsePrint();

    ExpressionNode* parseVariableOrNumber();

    ExpressionNode* parseFormula();

    ExpressionNode* parseParentheses();

    ExpressionNode* parseLoop();

    int run(ExpressionNode* node);
};