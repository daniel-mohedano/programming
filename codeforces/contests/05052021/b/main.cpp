#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <unordered_map>

using namespace std;

void test_case(){
    int n;
    scanf("%d", &n);
    int max = 9;
    int count = 0;
    while (max < n){
        count += 9;
        max = max*10 + 9;
    }

    int digits = floor(log10(n));
    int min_unit = 1;
    for (int i = 0; i < digits; ++i){
        min_unit = min_unit*10 + 1;
    }
    int min = min_unit;
    while(min <= n){
        ++count;
        min += min_unit;
    }
    cout << count << endl;
}

int main(){
    int t;
    scanf("%d", &t);
    while (t--){
        test_case();
    }
    return 0;
}
