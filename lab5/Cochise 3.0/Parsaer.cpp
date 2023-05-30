#include "Parsaer.h"
#include <cstddef>
#include <iostream>
#include <ostream>
#include <regex>
#include <stdexcept>
#include <type_traits>
#include <vector>
#include <set>

union returnVal
{
    int intVal;
};

map<string, TokenType*> tokenTypeLists = 
{
    {"NUMBER", new TokenType("NUMBER", regex("^[0-9].*"))},
    {"VARIABLE", new  TokenType("VARIABLE", regex("^[a-z].*"))},
    {"SEMICOLON",new  TokenType("SEMICOLON", regex("^[;]"))},
    {"SPACE",new TokenType("SPACE", regex("^[\\n\\t\\r]"))},
    {"ASSIGN",new TokenType("ASSIGN", regex("^[=]"))},
    {"PRINT",new  TokenType("PRINT", regex("^PRINT"))},
    {"PLUS",new  TokenType("PLUS", regex("^[+]"))},
    {"MINUS",new  TokenType("MINUS", regex("^[-]"))},
    {"LPAR",new  TokenType("LPAR", regex("^[\\(]"))},
    {"RPAR",new  TokenType("RPAR", regex("^[\\)]"))},
    {"TILL",new TokenType("TILL", regex("^TILL"))},
    {"LGAP",new TokenType("LGAP", regex("^[\\[]"))},
    {"RGAP",new TokenType("RGAP", regex("^[\\]]"))},
    {"FOR",new TokenType("FOR", regex("^FOR"))},
    {"NONE",new  TokenType("NONE", regex("^NONE"))}
};

Token Parser::match(vector<TokenType> expected)
{
    if (this->pos < this->tokens.size())
    {
        // pos = 0
        // pos = 0
        const Token currentToken = this->tokens[this->pos];
        // currentToken.Type.Name = "VAR"
        // currentToken.Type.Name = "VAR"
        // currentToken.Type.Name = "ASSIGN"
        for (vector<TokenType>::iterator it = expected.begin(); it != expected.end(); it++)
        {
            if (it->Name == currentToken.Type.Name)
            {
                this->pos+=1;
                return currentToken;
            }
        }
        
    }
    return Token(TokenType("NONE", regex("^NONE")), "", -1);
}

Token Parser::require(vector<TokenType> expected)
{
    //pos = 3
    Token token = this->match(expected);
    //pos = 4, token.type.name = "SEMICOLON"
    if (token.Type.Name == "NONE")
    {
        cout << "at:" <<this->pos <<endl;
        throw invalid_argument("require error");
    }
    return token;
}

ExpressionNode* Parser::parsePrint()
{
    Token operPrint = this->match({*tokenTypeLists["PRINT"]});
    if (operPrint.Type.Name != "NONE")
    {
        return new UnarOperatorNode(operPrint, this->parseFormula());
    }
    throw invalid_argument("PrintNode error");
}

ExpressionNode* Parser::parseParentheses()
{
    if (this->match({*tokenTypeLists["LPAR"]}).Type.Name != "NONE")
    {
        ExpressionNode* node = this->parseFormula();
        this->require({*tokenTypeLists["RPAR"]});
        return node;
    }
    else 
    {
        return this->parseVariableOrNumber();
    }
}

ExpressionNode* Parser::parseFormula()
{
    //pos = 2
    //Pos = 2
    ExpressionNode* leftNode = this->parseParentheses();
    //pos = 3, leftNode = NumberNode("1")
    //Pos = 3, leftNode = NumberNode("1")
    vector<TokenType> operators = {*tokenTypeLists["PLUS"], *tokenTypeLists["MINUS"]};
    Token oper = this->match(operators);
    //cout << oper.Type.Name << endl;
    //cout << "this:" << this->pos << endl;
    //Pos = 4 oper = PLUS
    while (oper.Type.Name != "NONE")
    {
        ExpressionNode* rightNode = this->parseParentheses();
        //Pos = 5 (a=1+1;<-), rightNode = NumberNode(1)
        leftNode = new BinOperatorNode(oper, leftNode, rightNode);
        oper = this->match({*tokenTypeLists["PLUS"], *tokenTypeLists["MINUS"]});
        //cout << "this:" << this->pos << endl;
    }
    return leftNode;
};

ExpressionNode* Parser::parseVariableOrNumber()
{
    //pos = 0
    //pos = 2
    //Pos = 2
    Token number = this->match({*tokenTypeLists["NUMBER"]});
    //Pos = 3
    //pos = 3, number.type.name = "Num"
    if (number.Type.Name != "NONE")
    {
        //pos = 2
        //pos = 3
        return new NumberNode(number);
    }
    //pos = 0
    Token variable = this->match({*tokenTypeLists["VARIABLE"]});
    //pos = 1, variable = Var("a")
    //Pos = 1
    if (variable.Type.Name != "NONE")
    {
        //cout << "var parsed";
    
        return new VariableNode(variable);
    }
    cout << this->pos << ":pos" << endl;
    throw invalid_argument("parsVarOrNum error\n");
};

ExpressionNode* Parser::parseLoop()
{
    ExpressionNode* iterator = this->parseVariableOrNumber();
    
    Token assign = this->match({*tokenTypeLists["ASSIGN"]});
    if (assign.Type.Name == "ASSIGN")
    {
        
        ExpressionNode* startNumber = this->parseVariableOrNumber(); //NumberNode
        ExpressionNode* startNode = new BinOperatorNode(assign, iterator, startNumber); // BinOperatorNode
        if (this->match({*tokenTypeLists["TILL"]}).Type.Name == "NONE"){
            throw invalid_argument("expected TILL");
        }
        ExpressionNode* endNumber = this->parseVariableOrNumber(); // NumberNode 10
        
        int Num = stoi(endNumber->getNumber().Text);
        if (this->match({*tokenTypeLists["LGAP"]}).Type.Name == "NONE"){
            throw invalid_argument("expected [");
        }
        
        StatementsNode* loopRootNode = new StatementsNode();
        while (this->match({*tokenTypeLists["RGAP"]}).Type.Name == "NONE")
        {
            ExpressionNode* codeStringNodeInLoop = this->parseExpression();
            loopRootNode->addNode(codeStringNodeInLoop);
            this->require({*tokenTypeLists["SEMICOLON"]});

        }
        LoopNode* loopAndStatement = new LoopNode(startNode, Num, loopRootNode);
        return loopAndStatement;
    }
    throw invalid_argument("parseLoop error");
};

ExpressionNode* Parser::parseExpression()
{
    //pos = 0, typeList(0) = var
    //Pos = 0
    
    if (this->match({*tokenTypeLists["VARIABLE"]}).Type.Name == "NONE")
    {
    if (this->match({*tokenTypeLists["PRINT"]}).Type.Name != "NONE"){
        this->pos -=1;
        ExpressionNode* printNode = this->parsePrint();
        //cout << "parsePrint";
        return printNode;
    }
    if (this->match({*tokenTypeLists["FOR"]}).Type.Name != "NONE"){
        ExpressionNode* iteratorAndNumberNode = this->parseLoop();
        this->pos-=1;
        this->require({*tokenTypeLists["RGAP"]});
        return iteratorAndNumberNode;
    }    
    }else{
    // pos = 1
    //Pos = 1
    this->pos-=1;
    //pos = 0
    //Pos=0
    cout << "here it is:" <<tokens[this->pos].Text<< endl;
    ExpressionNode* variableNode = this->parseVariableOrNumber();
    //Pos = 1
    //pos = 1, variableNode = VarNode("a")
    Token assignOperator = this->match({*tokenTypeLists["ASSIGN"]});
    //pos = 2, assignOperator.Type.Name = "ASSIGN"
    //Pos = 2
    if (assignOperator.Type.Name != "NONE")
    {
        //pos = 2, assignOperator.Type.Name = "ASSIGN"
        ExpressionNode* rightFormulaNode = this->parseFormula();
        //pos = 3, rightFormulaNode = NumberNode("1")
        ExpressionNode* binaryNode = new BinOperatorNode(assignOperator, variableNode, rightFormulaNode);
        return binaryNode;
    }}
    //cout << this->pos << endl;  
    throw invalid_argument("parseExp error");
};

ExpressionNode* Parser::parseCode()
{
    StatementsNode* root = new StatementsNode();
    while (this->pos < this->tokens.size())
    {
        //у нас есть список токенов 
        //Pos=0
        ExpressionNode* codeStringNode = this->parseExpression();
        //pos = 3, codeStringNode = BinNode(oper("="), varNode("a"), NumNode("1"))
        this->require({*tokenTypeLists["SEMICOLON"]});
        root->addNode(codeStringNode);
    };
    return root;

};// 


int Parser::run(ExpressionNode* node)
{
    //returnVal value;
    //cout << node;
    if (typeid(*node) == typeid(NumberNode))
    {
        return stoi(node->getNumber().Text);
    };
    if (typeid(*node) == typeid(UnarOperatorNode))
    {
        string operName = node->getOperator().Name;
        if (operName == "PRINT")
        {
            cout << this->run(node->getOperand());
            return 1;
        } 
    }
    if (typeid(*node) == typeid(BinOperatorNode))
    {
        string operName = node->getOperator().Name;
        if (operName == "PLUS")
        {
            return this->run(node->getLeftNode()) + this->run(node->getRightNode());
        }
        else if(operName == "MINUS")
        {
            return this->run(node->getLeftNode()) - this->run(node->getRightNode());
        }
        else if (operName == "ASSIGN")
        {
            auto result = this->run(node->getRightNode());
            auto variableNode = node->getLeftNode();
            this->scope[variableNode->getVariable().Text] = result;
            return result;
        }
    }
    if (typeid(*node) == typeid(VariableNode))
    {
        //cout << "YES" << endl;
        if(this->scope[node->getVariable().Text])
        {
            return scope[node->getVariable().Text];
        }
        else 
        {
            throw invalid_argument("нет такой переменной");
        }
    }
    if (typeid(*node) == typeid(StatementsNode))
    {
        //cout << "here is st" << endl;
        string nodeName = node->getNodeName();
        //cout << nodeName << endl;
        vector<ExpressionNode*> codeStrings = node->getCodeStrings();

        for (int i = 0; i < codeStrings.size(); i++)
        {

            ExpressionNode* node = codeStrings[i];
            //cout << i << ":" << codeStrings.size() << endl;
            this->run(node);
            //cout << "here it is" << endl;
        }
        return 1;
        // for (vector<ExpressionNode>::iterator it = codeStrings.begin(); it != codeStrings.end(); it++)
        // {
        //     ExpressionNode* node = it;
        //     this->run(node);
        //     return 1;
        // }    
    }
    if (typeid(*node) == typeid(LoopNode))
    {
        // есть: node->getIteratorStart()->getRightNode()->getNumber().Text
        // node->getEndNumber()
        // node->getIteratorStart()
        this->run(node->getIteratorStart());
        //i+1
        Token plusNumber = Token(*tokenTypeLists["NUMBER"], "1", -1);
        Token plus = Token(*tokenTypeLists["PLUS"], "+", -1);
        Token assign = Token(*tokenTypeLists["ASSIGN"], "=", -1);
        
        BinOperatorNode* plusNode = new BinOperatorNode(plus, node->getIteratorStart()->getLeftNode(),new NumberNode(plusNumber));
        //i=i+1
        BinOperatorNode* iteratorPlusNode = new BinOperatorNode(assign, node->getIteratorStart()->getLeftNode(), plusNode);
        int startValue = stoi(node->getIteratorStart()->getRightNode()->getNumber().Text);
        for (int i=startValue; i<node->getEndNumber(); i++)
        {
            this->run(node->getLoopNode());
            this->run(iteratorPlusNode);
        }
        return 1;
    }

    throw invalid_argument("run ERROR");
    return 1;
};




