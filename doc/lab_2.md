# ЛР \#2: [C++ & UNIX]: C++ BUILD / IF / LOOP, PYTHON #

Карсаков Григорий Вячеславович, 3 курс (ФизФ ИТМО), Z33434, 2023

## Цель ##

Познакомить студента с принципами компиляции исходного кода. Составить
программу с использованием циклов, условий и функций. Сравнить быстродействие
между C++ и Python. Ознакомление с типами данных.

## Решение ##

1. [С++ EXPRESSION] Создать и скомпилировать программу на C++.

Результат сборки (компиляции) сохранять в папку build. Папку build сделать
игнорируемой для GIT. Программа должна получать на вход число – это
количество итераций для выполнения расчета. В рамках итерации выполнять
следующее вычисление: x ^2- x ^2+ x *4- x *5+ x + x . Вычисление выполнять в виде
отдельной от main функции, которая будет вызвана циклически из main.
Фиксировать время выполнения программы, затрачиваемое на расчет выражения
n раз (n задается в консоли перед вычислением). Предусмотреть дополнительный
цикл на повторную итерацию запуска программы вычислений. Если было введено
не число, то завершить выполнение программы.

Код на C++:

```C++
#include <iostream> //standart
#include <cmath> //for pow()
#include <time.h> //magure time
#include <stdlib.h> // random number from _start to _end

using namespace std;

// int [−2 147 483 648:2 147 483 647] 4 bytes
// long 8 bytes

double func(const int &x, const int &n)
{
    clock_t start = clock(); // time of start in flops
    for(int i; i < n; i++) // new i; i=0,1,...,n; i = i+1
    {
        float res = pow(x, 2) - pow(x, 2) + x * 4 - x * 5 + x + x; //float result
    }
    clock_t end = clock(); // time of end in flops
    double seconds = (double)(end - start) / CLOCKS_PER_SEC; // megured time in flobs / flops per second
    std::cout << seconds << endl;
    printf("The time: %.5e seconds\n", seconds); // print  megured time in seconds
    return seconds; //return megured time in seconds
}

int main()
{
    string answer = "y"; //set answer
    while (answer == "y") // while loop, if snaswer != 'n', then breack
    {
        float x = rand() % 2+100; // randem number from 0 to 1
        // ask for input
        int n; 
        std::cout << "Enter the number of loops:" << endl;
        std::cin >> n;
        // is the input acceptable
        if(!std::cin.good()) // !std::cin.good('y') = False
        {
            std::cout << "Thats not int" << endl;
            return 0; // break
        }
        std::cout << "Thats int" << endl; // all good
        double res =  func(x, n);
        std::cout << "Again [y/n]?" << endl; // ask for another loop
        std::cin >> answer;
    }
}
```

2.[PYTHON EXPRESSION] Создать и скомпилировать программу на Python 3.

Результат сборки (компиляции) сохранять в папку build. Папку build сделать
игнорируемой для GIT. Программа должна получать на вход число – это
количество итераций для выполнения расчета. В рамках итерации выполнять
следующее вычисление: x ^2- x ^2+ x * 4 - x * 5+ x + x . Вычисление выполнять в виде
отдельной от main функции, которая будет вызвана циклически из main.
Фиксировать время выполнения программы, затрачиваемое на расчет выражения
n раз (n задается в консоли перед вычислением). Предусмотреть дополнительный
цикл на повторную итерацию запуска программы вычислений. Если было введено
не число, то завершить выполнение программы.

Код на Python:

```python
import numpy as np
import timeit

x = np.random.random()

def func(x):
    return x ** 2 - x ** 2 + x * 4 - x * 5 + x + x

def time_exp():
    inputn = input('Enter the number of loops:')
    try:
        n = int(inputn)
        print('Thats int.')
    except ValueError:
        print('Thats not int.')
        return None
    time = timeit.timeit(stmt='func(x)', globals={"func": func, "x": x}, number=n)
    return (n, time)

while True:
    res = time_exp()
    if res == None:
        break
    print("Time of %i loops is %.2e sec."%res)
    answer = str(input('again [y/n]?'))
    if answer != 'y':
        break 
```

## Вывод ##

Для того, чтобы определить, насколько быстро работает `C++`, нежели `Python`, проведем много экспериментов:

![Getting Started](6sem_Cpp_and_unixlab2/Python/conclusion.png)

Как можно видеть, время выполнения на `C++` на порядок меньше, чем на `Python`. Для объяснения результата можно выделить 3 причины:

### GIL (Global Interpreter Lock, глобальная блокировка интерпретатора) ###

Появляется, когда программа использует несколько потоков, которые обращаются к одним переменным (взято [отсюда](http://dabeaz.blogspot.com/2010/01/python-gil-visualized.html)).

![что-то](6sem_Cpp_and_unix/lab2/GIL.png)

Вот как это выглядит в случае использования двух потоков, интенсивно нагружающих процессов. Однако это не касается нашего случая.

### Python — интерпретируемый язык ###

 Большую часть времени (если только вы не пишете код, который запускается лишь один раз) Python занимается выполнением готового байт-кода, который сам же и пошёл.

 Альтернативой является JIT-компиляция

 ### Python — динамически типизированный язык ###

Однако тут нас замедляет сама динамическая типизация, а архитектура, позволявшая это.

* Каждый раз, когда выполняется обращение к переменной, её чтение или запись, производится проверка типа.

* Такой язык сложно оптимизировать.

Выводы сделаны по [мотивам](https://itnan.ru/post.php?c=1&p=418823).
