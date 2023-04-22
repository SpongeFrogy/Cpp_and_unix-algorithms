
# ЛР #4: [C++ & UNIX]: C++ PROCESSES / THREADS

Карсаков Григорий Вячеславович, 3 курс (ФизФ ИТМО), Z33434, 2023

## Цель

Познакомить студента с принципами параллельных вычислений. Составить несколько
программ в простейшими вычислительными действиями, чтобы освоить принципы
параллельных вычислений (когда одни алгоритмы зависят / не зависят от других).

## Решение

1. [С++ SEQUENCE] Последовательные вычисления

Требуется последовательно выполнить вычисления по формуле 1, вычисления по
формуле 2, после чего выполнить вычисления по формуле 3, которые выглядят
следующим образом: результат вычислений 1 + результат вычислений 2 –
результат вычислений 1
Выполнить последовательно на 10 000 итераций и 100 000 итераций:

- Формула 1: `f(x) = x ^2- x ^2+ x *4- x *5+ x + x`
- Формула 2: `f(x) = x + x`

Вывести длительность выполнения всех 10 000 итераций и 100 000 итераций в сек.

```C++
double func1(const double &x)
{
double y = pow(x, 2) - pow(x, 2) + pow(x, 4) - pow(x, 5) + x + x;
return y;
}


// 
double func2(const double &x)
{
double y = x + x;
return y;
}

double func3(const double &res1, const double &res2)
{
double y = res1 + res2 - res1;
return y;
}



double time1_s(const double &x, const int &n)
{
clock_t start = clock();
for(int i; i < n; i++)
{
    double res1 = func1(x);
    this_thread::sleep_for(chrono::milliseconds(10));
    double res2 = func2(x);
    this_thread::sleep_for(chrono::milliseconds(10));
    double res3 = func3(res1, res2);
}
clock_t end = clock(); // time of end in flops
double seconds = (double)(end - start) / CLOCKS_PER_SEC;
return seconds;
}

double time1(const double &x, const int &n)
{
clock_t start = clock();
for(int i; i < n; i++)
{
    double res1 = func1(x);
    double res2 = func2(x);
    double res3 = func3(res1, res2);
}
clock_t end = clock(); // time of end in flops
double seconds = (double)(end - start) / CLOCKS_PER_SEC;
return seconds;
}

int main()
{
double x = 1;
int n = 1000;

double sec1 = time1(1, n);
cout<< sec1 <<"s., N="<<n<<"\t"<<"без задержки"<<endl;

n = 100;
double sec2 = time1_s(1, n);
cout<< sec2 <<"s., N="<<n<<"\t"<<"с задержкой: 0.01s."<<endl;

return 0;
}
```

2. [C++ THREADS] Параллельные вычисления через потоки

Требуется параллельно (насколько возможно с помощью потоков) выполнить
вычисления по формуле 1, вычисления по формуле 2, после чего выполнить
вычисления по формуле 3, которые выглядят следующим образом: результат
вычислений 1 + результат вычислений 2 – результат вычислений 1
Выполнить последовательно на 10 000 итераций и 100 000 итераций

- Формула 1: `f(x) = x ^2- x ^2+ x *4- x*5+ x + x`
- Формула 2: `f(x) = x + x`

Вывести длительность выполнения всех 10 000 итераций и 100 000 итераций в сек.
в разбивке по шагам вычислений 1, 2 и 3

## Вывод

Результаты без задержки:
|**N**    |**straight time, s.**|**threads time, s.**|**processes time, s.**|
|---------|:-------------------:|--------------------|----------------------|
| 10 000  | <0.001              | 1.54               | 3                    |
| 100 000 | 0.003               | 15.823             | 3                    |

Результаты с задержкой 0.01 с.
|**N**    |**straight time, s.**|**threads time, s.**|**processes time, s.**|
|---------|:-------------------:|--------------------|----------------------|
| 100     | 3.182               | 0.674              | 3                    |
| 1 000   | 32.142              | 15.087             | 3                    |
