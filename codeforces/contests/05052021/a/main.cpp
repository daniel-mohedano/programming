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
    scanf("%d\n", &n);
    vector<char> tasks;
    char temp;
    int flag = 1;
    for (int i = 0; i < n; ++i){
        scanf("%c", &temp);
        if (flag){
            if (find(tasks.begin(), tasks.end(), temp) == tasks.end()) 
                tasks.push_back(temp);
            else{
                if (tasks.back() != temp) flag = 0;
            }
        }
    }
    if (flag) cout << "YES" << endl;
    else cout << "NO" << endl;
}

int main(){
    int t;
    scanf("%d", &t);
    while (t--){
        test_case();
    }
    return 0;
}
