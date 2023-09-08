#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

void heapify(vector<int>& arr, int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    if (l < n && arr[l] > arr[largest])
        largest = l;

    if (r < n && arr[r] > arr[largest])
        largest = r;

    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

vector<int> kLargest(vector<int>& arr, int k) {
    vector<int> res;

    make_heap(arr.begin(), arr.end());

    for (int i = 0; i < k; i++) {
        res.push_back(arr.front());
        pop_heap(arr.begin(), arr.end() - i);
    }

    return res;
}

int main() {
    vector<int> arr = { 12, 11, 13, 5, 6, 7 };
    int k = 3;

    make_heap(arr.begin(), arr.end());

    vector<int> res = kLargest(arr, k);

    cout << "k largest elements: ";
    for (int i = 0; i < k; i++) {
        cout << res[i] << " ";
    }

    return 0;
}