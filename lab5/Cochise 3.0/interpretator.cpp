#include "Parsaer.h"
#include <vector>
#include <fstream>
#include <thread>

int main(int argc, char* argv[])
{

string code = "";
string name;
if (argc > 1)// если передаем аргументы, то argc будет больше 1(в зависимости от кол-ва аргументов)
       {
             name = argv[1];// вывод второй строки из массива указателей на строки(нумерация в строках начинается с 0 )
       } else
               {
                 cout << "Not arguments" << endl;
      }


ifstream file(name);
string line;
ifstream f(name); //taking file as inputstream
if(f) {
      ostringstream ss;
      ss << f.rdbuf(); // reading data
      code = ss.str();
}
//cout<< code << endl;

Laxer lexer = Laxer(code);

lexer.lexAnalysis();

// for (vector<Token>::iterator it = lexer.tokenList.begin(); it !=lexer.tokenList.end(); it++)
// {
//     cout<< it->Type.Name + ";" << it->Pos  <<";"<< it->Text << endl; 
// }

int pos_token = 0;
vector<vector<Token>> threadsCode;

while (pos_token < lexer.tokenList.size()) {
vector<Token> oneThreadCode;
while (lexer.tokenList[pos_token].Type.Name != "THREAD" and pos_token < lexer.tokenList.size()) {

    oneThreadCode.push_back(lexer.tokenList[pos_token]);
    pos_token+=1;

}
threadsCode.push_back(oneThreadCode);
pos_token+=1;
}
thread t1([&threadsCode](){
        Parser parser = Parser(threadsCode[0]);
        auto rootNode = parser.parseCode();
        parser.run(rootNode);
    });
t1.join();
if (threadsCode.size() > 1){
    thread t2([&threadsCode](){
        Parser parser = Parser(threadsCode[1]);
        auto rootNode = parser.parseCode();
        parser.run(rootNode);
    });
    t2.join();
}
if (threadsCode.size() > 2){
    thread t3([&threadsCode](){
        Parser parser = Parser(threadsCode[2]);
        auto rootNode = parser.parseCode();
        parser.run(rootNode);
    });
    t3.join();
}
// Parser parser = Parser(lexer.tokenList);

// auto rootNode = parser.parseCode();

// //cout << rootNode->getNodeName() << endl;

// parser.run(rootNode);



return 1;
}

