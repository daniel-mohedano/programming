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
    if (n == 1) cout << "1" << endl;
    else if (n == 2) cout << "-1" << endl;
    else{
        vector<int> matrix(n*n, 0);
        for (int i = 1; i <= n*n; ++i){
            if (matrix[(i-1)*2 % (n*n)] == 0)
                matrix[(i-1)*2 % (n*n)] = i;
            else
                matrix[(i-1)*2 % (n*n) + 1] = i;
        }

        for (int i = 0; i < n; ++i){
            for (int j = 0; j < n; ++j){
                cout << matrix[n*i+j] << " ";
            }
            cout << endl;
        } 
    }
}

int main(){
    int t;
    scanf("%d", &t);
    while (t--){
        test_case();
    }
    return 0;
}
