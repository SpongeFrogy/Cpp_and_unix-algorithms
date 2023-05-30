#include "TokenType.h"
#include <vector>

// vector<TokenType> tokenTypeListValues = 
// {
//     TokenType("NUMBER", regex("[0-9]*")),
//     TokenType("VARIABLE", regex("[a-z]*")),
//     TokenType("SEMICOLON", regex(";")),
//     TokenType("SPACE", regex("[\\n\\t\\r]")),
//     TokenType("ASSIGN", regex("=")),
//     TokenType("PRINT", regex("PRINT")),
//     TokenType("PLUS", regex("+")),
//     TokenType("MINUS", regex("-")),
//     TokenType("LPAR", regex("\\(")),
//     TokenType("RPAR", regex("\\)"))
//  };

// map<string, TokenType> tokenTypeList = 
// {
//     {"NUMBER", TokenType("NUMBER", regex("[0-9]*"))},
//     {"VARIABLE",  TokenType("VARIABLE", regex("[a-z]*"))},
//     {"SEMICOLON", TokenType("SEMICOLON", regex(";"))},
//     {"SPACE", TokenType("SPACE", regex("[\\n\\t\\r]"))},
//     {"ASSIGN", TokenType("ASSIGN", regex("="))},
//     {"PRINT", TokenType("PRINT", regex("PRINT"))},
//     {"PLUS", TokenType("PLUS", regex("+"))},
//     {"MINUS", TokenType("MINUS", regex("-"))},
//     {"LPAR", TokenType("LPAR", regex("\\("))},
//     {"RPAR", TokenType("RPAR", regex("\\)"))}
// };

// TokenType* tokenTypeList(string tokenName)
// {
//     if (tokenName == "NUMBER") return new TokenType("NUMBER", "[0-9]*");
//     if (tokenName == "VARIABLE") return new TokenType("VARIABLE", "[a-z]*");
//     if (tokenName == "SEMICOLON") return new TokenType("SEMICOLON", ";");
//     if (tokenName == "SPACE") return new TokenType("SPACE", "[\\n\\t\\r]");
//     if (tokenName == "ASSIGN") return new TokenType("ASSIGN", "=");
//     if (tokenName == "PRINT") return new TokenType("PRINT", "print");
//     if (tokenName == "PLUS") return new TokenType("PLUS", "+");
//     if (tokenName == "MINUS") return new TokenType("MINUS", "-");
//     if (tokenName == "LPAR") return new TokenType("LPAR", "\\(");
//     if (tokenName == "RPAR") return new TokenType("RPAR", "\\)");
//     return new TokenType("NONE", "none");
// };