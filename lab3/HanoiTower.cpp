#include<iostream>
#include<string>
#include<list>

using namespace std;

template<typename T>
void printList(std::list<T> l) {
    for (const auto &item : l) {
<<<<<<< HEAD
        cout << item << "; ";
=======
        cout << item << "; " << endl;
>>>>>>> main
    }
    cout << endl;
}
  
std::list<string> towerOfHanoi(int n, char from_rod, char to_rod,
                  char aux_rod,std::list<string> list) //функция возвращает список действий
<<<<<<< HEAD
{
    if (n == 0) {
        return list;
    }
    list = towerOfHanoi(n - 1, from_rod, aux_rod, to_rod, list);
    //cout << "Move disk " << n << " from rod " << from_rod
    //     << " to rod " << to_rod << endl;
=======
{   cout<< n<< "f"<< from_rod<< to_rod << endl;
    if (n == 0) {
        return list;
    }
    cout<< n<< "s"<< from_rod<< to_rod << endl;
    list = towerOfHanoi(n - 1, from_rod, aux_rod, to_rod, list);
    //cout << "Move disk " << n << " from rod " << from_rod
    //     << " to rod " << to_rod << endl;
    cout<<n<<"th"<< from_rod<< to_rod << endl;
>>>>>>> main
    string s = to_string(n).append(":");
    s+=from_rod;
    s.append("->");
    s+=to_rod;
    list.push_back(s);
    list = towerOfHanoi(n - 1, aux_rod, to_rod, from_rod, list);
<<<<<<< HEAD
=======
    cout<<n<<"fo"<< from_rod<< to_rod << endl;
>>>>>>> main
    return list;
}
  
int main()
{
<<<<<<< HEAD
    int N = 8;
=======
    int N = 2;
>>>>>>> main
    std::list<string> l = {};
    // A, B and C are names of rods
    l = towerOfHanoi(N, 'A', 'C', 'B', l);
    printList(l);
<<<<<<< HEAD
=======
    l.clear(); //удаляем из памяти
>>>>>>> main
    return 0;
}