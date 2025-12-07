#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <map>
#include <unordered_map>

using namespace std;

void test_case(){
    int n, w;
    cin >> n >> w;
    map<int, int, greater<int>> blocks;
    int temp;
    for (int i = 0; i < n; ++i) {
        cin >> temp;
        if (blocks.find(temp) == blocks.end()) blocks.insert(pair<int,int>(temp, 1));
        else ++(blocks.find(temp)->second);
    }

    int h = 0;
    int current_w = 0;
    while(blocks.size() != 0){
        int flag = 0;
        for (auto& x: blocks){
            if (x.first <= w-current_w){
                flag = x.first;
                int amount = floor(1.0 * (w-current_w) / x.first);
                current_w += (x.first * min(amount, x.second));
                x.second -= min(amount, x.second);
                if (current_w == w){
                    ++h;
                    current_w = 0;
                    break;
                }
            }
        }
        if (flag == 0) {
            ++h;
            current_w = 0;
        }else{
            if (blocks.find(flag)->second == 0) blocks.erase(flag);
        }
    }
    if (current_w != 0) ++h;
    cout << h << endl;
}

int main(){
    int t;
    cin >> t;
    while(t--){
        test_case();
    }
    return 0;
}
