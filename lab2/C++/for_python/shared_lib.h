#ifndef SHARED_LIB_H
#define SHARED_LIB_H

#include <iostream>
#include <cmath>
#include <time.h>

#ifdef __cplusplus
    extern "C" {
#endif

#ifdef BUILD_MY_DLL
     #define SHARED_LIB __declspec(dllexport)
#else
     #define SHARED_LIB __declspec(dllimport)
#endif

double func(double x, long n);

#ifdef __cplusplus
    }
#endif

#endif 