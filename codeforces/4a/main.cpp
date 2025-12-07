#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>

using namespace std;

int main(){
    int w;
    cin >> w;
    if((w % 2) == 0 && w > 3) cout << "YES" << endl;
    else cout << "NO" << endl;
    return 0;
}
