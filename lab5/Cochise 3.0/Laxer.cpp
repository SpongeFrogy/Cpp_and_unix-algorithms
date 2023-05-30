#include "Laxer.h"
#include <exception>
#include <regex>
#include <stdexcept>

vector<TokenType> tokenTypeListValues = 
{
    TokenType("NUMBER", regex("^[0-9]*")),
    TokenType("VARIABLE", regex("^[a-z]*")),
    TokenType("SEMICOLON", regex("^[;]")),
    TokenType("SPACE", regex("^[\\n\\t\\r\\s]")),
    TokenType("ASSIGN", regex("^[=]")),
    TokenType("PRINT", regex("^PRINT")),
    TokenType("PLUS", regex("^[+]")),
    TokenType("MINUS", regex("^[-]")),
    TokenType("LPAR", regex("^[\\(]")),
    TokenType("RPAR", regex("^[\\)]")),
    TokenType("TILL", regex("^TILL")),
    TokenType("LGAP", regex("^[\\[]")),
    TokenType("RGAP", regex("^[\\]]")),
    TokenType("FOR", regex("^FOR")),
    TokenType("THREAD", regex("^THREAD"))
 };

map<string, TokenType> tokenTypeList = 
{
    {"NUMBER", TokenType("NUMBER", regex("^[0-9].*"))},
    {"VARIABLE",  TokenType("VARIABLE", regex("^[a-z].*"))},
    {"SEMICOLON", TokenType("SEMICOLON", regex("^[;]"))},
    {"SPACE", TokenType("SPACE", regex("^[\\n\\t\\r]"))},
    {"ASSIGN", TokenType("ASSIGN", regex("^[=]"))},
    {"PRINT", TokenType("PRINT", regex("^PRINT"))},
    {"PLUS", TokenType("PLUS", regex("^[+]"))},
    {"MINUS", TokenType("MINUS", regex("^[-]"))},
    {"LPAR", TokenType("LPAR", regex("^[\\(]"))},
    {"RPAR", TokenType("RPAR", regex("^[\\)]"))},
    {"TILL", TokenType("TILL", regex("^TILL"))},
    {"LGAP", TokenType("LGAP", regex("^[\\[]"))},
    {"RGAP", TokenType("RGAP", regex("^[\\]]"))},
    {"FOR", TokenType("FOR", regex("^FOR"))},
    {"THREAD", TokenType("THREAD", regex("^THREAD"))}
};



vector<Token> Laxer::lexAnalysis()
{
    while (this->nextToken())
    {
        // cout<<"Token"<<endl;
    }
    return this->tokenList;
};

bool Laxer::nextToken()
{
    if (this->pos >= this->Code.size()) return false;
    for (vector<TokenType>::iterator it = tokenTypeListValues.begin(); it != tokenTypeListValues.end(); it++)
    {
        auto tokenType = *it;
        cmatch match;
        const bool result = regex_search(this->Code.substr(this->pos).c_str(), match, tokenType.Regex);
        //cout<<result<<endl;
        
        // cout<<"->"<<match[0].str()<<"<-"<<endl;
        // const bool result = regex_match(this->Code.substr(this->pos), match, tokenType.Regex);
        if (result && match[0].str().size()>0)
        {
            // cout<<tokenType.Name<<endl;
            // cout<<match[0].str()<<endl;
            const Token token = Token(tokenType, match[0], this->pos);
            this->pos+=match[0].str().size();
            if (token.Type.Name != "SPACE")
            {
                this->tokenList.push_back(token);
            }
            return true;
        }
    }
    throw invalid_argument("Code Error");
};