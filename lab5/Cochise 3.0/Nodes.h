#include "Laxer.h"
#include <stdexcept>
#include <string>
#include <vector>

class ExpressionNode
{
    public:
    virtual Token getNumber() {throw invalid_argument("no getNumber");};
    virtual string getNodeName() {throw invalid_argument("no getNodeName");};
    virtual TokenType getOperator() {throw invalid_argument("no getOperator");};
    virtual ExpressionNode* getOperand() {throw invalid_argument("no getOperand");};
    virtual Token getVariable() {throw invalid_argument("no getNumber");};
    virtual ExpressionNode* getLeftNode() {throw invalid_argument("no getLeftNode");};
    virtual ExpressionNode* getRightNode() {throw invalid_argument("no getRightNode");};
    virtual vector<ExpressionNode*> getCodeStrings() {throw invalid_argument("no getCodeStrings");};
    virtual string VariableOrNumberNode(){return "no";};
    virtual string getVariableOrNumber(){throw invalid_argument("no gotVariableOrNumber");}

    virtual ExpressionNode* getLoopNode(){throw invalid_argument("no getLoopNode");};
    virtual ExpressionNode* getIteratorStart(){throw invalid_argument("no getIteratorStart");};
    virtual int getEndNumber(){throw invalid_argument("no getEndNumber");};
    
    

};

class StatementsNode: public ExpressionNode
{
    public:
    string getNodeName(){return "Statements";};
    vector<ExpressionNode*> codeStrings;
    void addNode(ExpressionNode* node)
    {
        this->codeStrings.push_back(node);
    };
    vector<ExpressionNode*> getCodeStrings(){return codeStrings;};
};

// class VariableOrNumberNode: public ExpressionNode
// {
//     public:;
// };

class VariableNode: public ExpressionNode
{
    public:
    Token variable;
    string getNodeName() override {return "Variable";};
    string getVariableOrNumber() override {return "Variable";};
    Token getVariable() override 
    {
        return variable;
    }
    VariableNode(Token var): variable(var)
    {}
};

class NumberNode: public ExpressionNode
{
    public:
    Token number;
    string nodeName = "NUMBER";
    string getNodeName(){return "Number";};
    string getVariableOrNumber(){return "Number";};
    NumberNode(Token num): number(num)
    {};
    Token getNumber(){return number;}
};

class BinOperatorNode: public ExpressionNode
{
    public:
    Token oper;
    ExpressionNode* leftNode;
    ExpressionNode* rightNode;
    string getNodeName(){return "Bin";};
    TokenType getOperator(){return oper.Type;}
    ExpressionNode* getLeftNode(){return leftNode;}
    ExpressionNode* getRightNode(){return rightNode;}

    BinOperatorNode(Token opr, ExpressionNode* left, ExpressionNode* right):
    oper(opr), leftNode(left), rightNode(right)
    {}

};

class UnarOperatorNode: public ExpressionNode
{
    public:
    Token oper;
    ExpressionNode* operand;
    string getNodeName(){return "Unar";};
    TokenType getOperator()
    {
        return oper.Type;
    }
    ExpressionNode* getOperand()
    {
        return operand;
    }
    UnarOperatorNode(Token opr, ExpressionNode* opd): oper(opr), operand(opd)
    {}
};

class LoopNode: public ExpressionNode
{
    public:
    StatementsNode* loopStrings;
    ExpressionNode* iteratorExp;
    int tillNumber;
    ExpressionNode* getLoopNode(){return loopStrings;};
    ExpressionNode* getIteratorStart(){return iteratorExp;};
    int getEndNumber(){return tillNumber;};
    LoopNode(ExpressionNode* i,int number, StatementsNode* loop):iteratorExp(i), tillNumber(number), loopStrings(loop){}

};