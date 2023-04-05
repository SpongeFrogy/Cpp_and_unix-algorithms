#include<iostream>
#include<string>
#include<list>

using namespace std;

template<typename T>
void printList(std::list<T> l) {
    for (const auto &item : l) {
        cout << item << "; " << endl;
    }
    cout << endl;
}
  
std::list<string> towerOfHanoi(int n, char from_rod, char to_rod,
                  char aux_rod,std::list<string> list) //функция возвращает список действий
{
    if (n == 0) {
        return list;
    }
    list = towerOfHanoi(n - 1, from_rod, aux_rod, to_rod, list);
    //cout << "Move disk " << n << " from rod " << from_rod
    //     << " to rod " << to_rod << endl;
    string s = to_string(n).append(":");
    s+=from_rod;
    s.append("->");
    s+=to_rod;
    list.push_back(s);
    list = towerOfHanoi(n - 1, aux_rod, to_rod, from_rod, list);
    return list;
}
  
int main()
{
    int N = 8;
    std::list<string> l = {};
    // A, B and C are names of rods
    l = towerOfHanoi(N, 'A', 'C', 'B', l);
    printList(l);
    l.clear(); //удаляем из памяти
    return 0;
}