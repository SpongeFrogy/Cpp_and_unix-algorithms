g++ -c -DBUILD_MY_DLL shared_lib.cpp -municode
g++ -shared -o shared_lib.dll shared_lib.o -Wl,--out-implib,libshared_lib.a