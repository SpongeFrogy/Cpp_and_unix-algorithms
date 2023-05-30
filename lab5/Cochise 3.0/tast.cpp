#include <algorithm>
#include <regex>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>

using namespace std;

class foo
{
  public:
  int num;
  virtual int ass(){throw invalid_argument("foo");};
  virtual string get(){return "from foo";}
};

class boo: virtual public foo
{
  public:
  int ass() override {cout << "ass"; return 1;};
  string get() override {return "from boo";};
  string s;
  boo(string S): s(S){};
};

foo* func()
{
  boo B("s");
  return new boo("s");
}

int main(int argc, char* argv[])
{
       if (argc > 1)// если передаем аргументы, то argc будет больше 1(в зависимости от кол-ва аргументов)
       {
             cout << argv[1]<<endl;// вывод второй строки из массива указателей на строки(нумерация в строках начинается с 0 )
       } else
               {
                 cout << "Not arguments" << endl;
      }
       //system("pause");
      return 0;
}
